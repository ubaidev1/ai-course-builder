from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Course, Lesson, QuizScore, Quiz


@login_required
def home_view(request):
    courses = Course.objects.all()
    course_progress = []
    for course in courses:
        total_quizzes = Quiz.objects.filter(lesson__module__course=course).count()
        completed_quizzes = QuizScore.objects.filter(
            user=request.user,
            quiz__lesson__module__course=course
        ).count()
        if total_quizzes > 0:
            progress_percentage = (completed_quizzes / total_quizzes) * 100
        else:
            progress_percentage = 0
        course_progress.append({
            'course': course,
            'progress': progress_percentage
        })

    return render(request, 'home.html', {'course_progress': course_progress})


@login_required
def next_lesson_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    next_lesson = get_next_lesson(course, request.user)
    return redirect('course_detail', course_id=course_id, lesson_id=next_lesson)


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
        return redirect('course_detail', course_id=lesson.module.course.id,
                        lesson_id=next_lesson)


def get_next_lesson(course, user):
    quizzes = Quiz.objects.filter(lesson__module__course=course)
    unattempted_quizzes = quizzes.exclude(
        Q(user_scores__user=user)
    )
    first_quiz = unattempted_quizzes.order_by('created_at').first()
    return first_quiz.lesson.id
