import base64

from django.contrib.auth.decorators import login_required
from django.core import signing
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from users.models import User, UserInvitation

from .models import Course, Lesson, QuizScore, Quiz, CourseEnrollment


def home_view(request, course_id=None):
    token = request.GET.get('token')
    if token:
        request.session['invitation_token'] = token
    if not request.user.is_authenticated:
        return redirect('/')
    token = request.session.pop('invitation_token', None)
    if token:
        token_data = signing.loads(token)
        admin_id = token_data.get('user_id')
        course_id = token_data.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        admin = get_object_or_404(User, id=admin_id)
        existing_enrollment = CourseEnrollment.objects.filter(user=request.user, course=course).exists()
        if not existing_enrollment:
            invitation_exists = UserInvitation.objects.filter(email=request.user.email, course=course,
                                                              admin=admin).exists()
            if not invitation_exists:
                UserInvitation.objects.create(email=request.user.email, admin=admin, course=course)
    invitations = UserInvitation.objects.filter(email=request.user.email, status=UserInvitation.PENDING)
    for invitation in invitations:
        CourseEnrollment.objects.create(
            invited_by=invitation.admin,
            course=invitation.course,
            user=request.user)
        invitation.status = UserInvitation.ACCEPTED
        invitation.save()
    course_progress = get_course_progress(request.user)
    progress = None
    quiz_score = None
    if course_id:
        course_data = next((cp for cp in course_progress if cp['course'].id == course_id), None)
        if course_data:
            progress = course_data['progress']

    return render(request, 'home.html', {
        'course_progress': course_progress,
        'progress': progress,
        'quiz_scores': quiz_score
    })


@login_required
def next_lesson_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    next_lesson = get_next_lesson(course, request.user)
    return redirect('course_detail', course_id=course_id, lesson_id=next_lesson)


@login_required
def retake_quiz(request, course_id):
    # Delete the user's existing quiz scores for the given course
    QuizScore.objects.filter(user=request.user, quiz__lesson__module__course_id=course_id).delete()
    course = get_object_or_404(Course, id=course_id)
    next_lesson = get_next_lesson(course, request.user)
    if next_lesson:
        return redirect('course_detail', course_id=course_id, lesson_id=next_lesson)
    else:
        return redirect('home')


@login_required
def course_detail_view(request, course_id, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quiz = lesson.quizzes.first()
    user_score = None
    quiz_data = {}
    if quiz:
        quiz_score = QuizScore.objects.filter(user=request.user, quiz=quiz).first()
        if quiz_score:
            user_score = quiz_score.score

        questions = quiz.questions.all()
        quiz_data = {
            "quiz": [
                {
                    "question": q.question_text,
                    "options": [opt.option_text for opt in q.options.all()],
                    "correct_answer": q.correct_answer
                }
                for q in questions
            ]
        }
        course = get_object_or_404(Course, id=course_id)
        next_lesson = get_next_lesson(course, request.user)
        return render(request, 'course_detail.html', {
            'course': course,
            'lesson': lesson,
            'user_score': user_score,
            'quiz_data': quiz_data,
            'next_lesson': next_lesson})


@login_required()
def submit_quiz_score(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quiz = lesson.quizzes.first()
    if not quiz:
        return JsonResponse({'error': 'No quiz available for this lesson.'}, status=404)
    if request.method == "POST":
        score = request.POST.get('final_score')
        QuizScore.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            defaults={'score': score})
        next_lesson = get_next_lesson(course, request.user)
        if not next_lesson:
            return redirect('home', course_id=course_id)
        return redirect('course_detail', course_id=lesson.module.course.id,
                        lesson_id=next_lesson)


def get_next_lesson(course, user):
    quizzes = Quiz.objects.filter(lesson__module__course=course)
    unattempted_quizzes = quizzes.exclude(
        Q(user_scores__user=user)
    )
    first_quiz = unattempted_quizzes.order_by('created_at').first()
    if first_quiz:
        return first_quiz.lesson.id


def get_course_progress(user):
    courses = Course.objects.filter(is_published=True, enrollment__user=user)
    if user.is_admin:
        courses = Course.objects.filter(is_published=True, created_by=user)
    course_progress = []
    for course in courses:
        total_quizzes = Quiz.objects.filter(lesson__module__course=course).count()
        completed_quizzes = QuizScore.objects.filter(
            user=user,
            quiz__lesson__module__course=course
        ).count()

        # Calculate course progress
        if total_quizzes > 0:
            progress_percentage = (completed_quizzes / total_quizzes) * 100
        else:
            progress_percentage = 0
        # Append the course data with progress and obtained score
        course_progress.append({
            'course': course,
            'progress': progress_percentage,
        })
    return course_progress
