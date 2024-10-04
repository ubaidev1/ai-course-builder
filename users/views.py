import base64
import json
import os

from antropic_api.anthropic_response import get_ai_course_details
from course.models import Course, Question, QuizScore, CourseEnrollment
from course.models import Lesson, Quiz, Question, Option, Module
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.db.models import Subquery
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from scripts.create_course import create_course
from scripts.extend_existing_course import extend_existing_course
from services import EmailServices
from users.models import User, CustomizationSettings
from users.models.invitations import UserInvitation


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not first_name or not last_name or not email or not password:
            messages.error(request, 'Please fill in all fields.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Already have an account, Please Login!')
        else:
            User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            return redirect('login')
    return render(request, 'signup.html')


def admin_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not first_name or not last_name or not email or not password:
            messages.error(request, 'Please fill in all fields.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
        else:
            User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name)
            return redirect('login')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Please fill in all fields.')
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def customize_color(request):
    settings, created = CustomizationSettings.objects.get_or_create(admin=request.user)
    print("********SETTINGS******IHHI")
    print(settings.navbar_color)
    print("****CREATED*****")
    print(created)

    if request.method == 'POST':
        settings.navbar_color = request.POST.get('navbar_color')
        print("*****NAVBAR COLOR***")
        print(request.POST.get('navbar_color'))
        settings.button_color = request.POST.get('button_color')
        settings.background_color = request.POST.get('background_color')
        settings.points_color = request.POST.get('points_color')
        settings.save()
        return redirect('customize_color')
    return render(request, 'customize.html', {'settings': settings})


@login_required
def dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    try:
        if request.method == 'POST' and request.FILES.get('pdf_file'):
            course_name = request.POST.get('course_name')
            pdf_file = request.FILES['pdf_file']
            fs = FileSystemStorage(location='/tmp')
            filename = fs.save(pdf_file.name, pdf_file)
            pdf_file_path = fs.path(filename)
            json_data = get_ai_course_details('config.json', pdf_file_path)
            data = json.loads(json_data)
            course = create_course(request.user, data, course_name)
            os.remove(pdf_file_path)
            return redirect('edit_course', course_id=course.id)

        courses = Course.objects.all()
        return render(request, 'dashboard.html', {'courses': courses})

    except Exception as e:
        return render(request, 'dashboard.html', {
            'courses': Course.objects.all(),
            'error_message': f"An unexpected error occurred: {str(e)}"
        })


@login_required
def edit_course(request, course_id):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    # Get the specific course to edit
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        course.title = request.POST.get('course_title')
        course.description = request.POST.get('course_description')
        course.save()
        messages.success(request, 'Course updated successfully!')
        return redirect('edit_course', course_id=course_id)

    # Render the edit form for the specific course
    return render(request, 'edit-courses.html', {'course': course})


@login_required
def delete_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        course.is_archived = True
        course.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def course_actions(request):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    context = {
        'courses': Course.objects.filter(created_by=request.user, is_archived=False),
    }
    return render(request, 'course_actions.html', context)


@login_required
def toggle_course_publish(request, course_id):
    if not request.user.is_admin:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    course = get_object_or_404(Course, id=course_id)
    course.is_published = not course.is_published
    course.save()
    return JsonResponse({'status': 'success', 'is_published': course.is_published})


@login_required
def result_view(request):
    results = []
    search_query = request.GET.get('search', '')
    selected_course_id = request.GET.get('course', '')
    current_admin = request.user
    if not current_admin.is_admin:
        return HttpResponseForbidden("You are not authorized to view this page.")
    courses = Course.objects.all()
    filtered_courses = courses
    if selected_course_id:
        filtered_courses = filtered_courses.filter(id=selected_course_id)
    invited_user_emails = UserInvitation.objects.filter(
        admin=current_admin,
        status=UserInvitation.ACCEPTED
    ).values_list('email', flat=True)

    invited_users = User.objects.filter(email__in=Subquery(invited_user_emails)).distinct()

    for course in filtered_courses:
        users = invited_users.filter(
            quiz_scores__quiz__lesson__module__course=course
        ).filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        ).distinct()
        for user in users:
            total_score = 0
            obtained_score = 0
            quizzes = course.modules.all().values_list('lessons__quizzes', flat=True)
            total_questions = Question.objects.filter(quiz__in=quizzes).count()
            total_score = total_questions * 10  # Each question is worth 10 marks
            # Calculate the obtained score
            latest_quiz_score = QuizScore.objects.filter(user=user, quiz__lesson__module__course=course) \
                .order_by('-created_at').first()
            if latest_quiz_score:
                obtained_score = latest_quiz_score.score
            percentage = (obtained_score / total_score) * 100 if total_score > 0 else 0
            results.append({
                'course': course.title,
                'username': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'obtained_score': obtained_score,
                'total_score': total_score,
                'percentage': percentage
            })
    context = {
        'results': results,
        'courses': courses,
        'search_query': search_query,
        'selected_course_id': selected_course_id,
    }
    return render(request, 'result.html', context)


@login_required
def send_invite(request, course_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        emails = data.get('email')
        course = get_object_or_404(Course, id=course_id)
        user_id = request.user.id
        token = signing.dumps({
            'course_id': str(course_id),
            'user_id': str(user_id)
        })
        invite_link = f"{request.build_absolute_uri(reverse('enroll_course', args=[course_id]))}?token={token}"

        if emails:
            try:
                for email in emails:
                    EmailServices.send_email_to_client(email, course, request.user, invite_link)
                    invitation.save()
            except Exception as e:
                print(e)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'success', 'invite_link': invite_link})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    token = request.GET.get('token')

    return render(request, 'enroll_course.html', {'course': course, 'token': token})


@login_required
def extend_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        # Handle PDF Upload for Extending Course
        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES.get('pdf_file')
            if not pdf_file:
                messages.error(request, "Please upload a PDF file.")
                return redirect('extend_course', course_id=course.id)

            fs = FileSystemStorage(location='/tmp')
            filename = fs.save(pdf_file.name, pdf_file)
            pdf_file_path = fs.path(filename)
            json_data = get_ai_course_details('config.json', pdf_file_path)
            data = json.loads(json_data)
            extend_existing_course(data, course)
            messages.success(request, f"Course '{course.title}' has been extended with new content.")
            os.remove(pdf_file_path)
            return redirect('course_actions')

        elif 'lesson_title' in request.POST:
            module_id = request.POST.get('module_id')
            lesson_title = request.POST.get('lesson_title')
            lesson_content = request.POST.get('lesson_content')
            quiz_title = request.POST.get('quiz_title')
            questions = request.POST.getlist('questions[]')
            correct_answers = request.POST.getlist('correct_answers[]')

            module = get_object_or_404(course.modules.all(), id=module_id)
            lesson = Lesson.objects.create(title=lesson_title, content=lesson_content, module=module)
            quiz = Quiz.objects.create(title=quiz_title, lesson=lesson)
            for i, question_text in enumerate(questions):
                correct_answer = correct_answers[i]
                options = request.POST.getlist(f'options_question{i + 1}[]')
                question = Question.objects.create(
                    quiz=quiz,
                    question_text=question_text,
                    correct_answer=correct_answer
                )
                for option in options:
                    Option.objects.create(question=question, option_text=option)
            messages.success(request, f"Lesson '{lesson_title}' and its quiz have been successfully added.")
            return redirect('extend_course', course_id=course.id)
    return render(request, 'extend_course.html', {'course': course})


def update_lesson(request, lesson_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lesson = Lesson.objects.get(id=lesson_id)
            lesson.title = data['title']
            lesson.content = data['content']
            lesson.save()
            return JsonResponse({'success': True})
        except Lesson.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lesson not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
def update_title(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_type = data.get('type')
        item_id = data.get('id')
        new_title = data.get('title')

        if item_type == 'module':
            try:
                module = Module.objects.get(id=item_id)
                module.title = new_title
                module.save()
                return JsonResponse({'success': True})
            except Module.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Module not found'})

        elif item_type == 'lesson':
            try:
                lesson = Lesson.objects.get(id=item_id)
                lesson.title = new_title
                lesson.save()
                return JsonResponse({'success': True})
            except Lesson.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Lesson not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt  # Only use this if CSRF tokens are not provided in the JavaScript
def update_quiz(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            field = data.get('field')
            new_value = data.get('value')

            # Determine if it's a question or an option
            if 'question' in field:
                # Update the question text
                question_id = field.split('-')[1]  # Get question ID from field name (if needed)
                quiz = Quiz.objects.get(id=question_id)  # Fetch the relevant quiz
                quiz.question = new_value
                quiz.save()

            elif 'option' in field:
                # Update the option text
                option_id = field.split('-')[1]  # Get option ID from field name (if needed)
                option = QuizOption.objects.get(id=option_id)  # Fetch the relevant option
                option.text = new_value
                option.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def save_quiz_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            field_type = data.get('field_type')
            print(field_type, "FIELD TYPE")
            updated_value = data.get('updated_value')
            question_index = data.get('question_index')
            lesson_id = data.get('lesson_id')

            # Find the quiz associated with the lesson
            lesson = Lesson.objects.get(id=lesson_id)
            quiz = Quiz.objects.get(lesson=lesson)
            questions = list(quiz.questions.all())
            if question_index is None:
                question_index = 0

            if question_index < len(questions):
                question = questions[question_index]
                if field_type == 'question':
                    question.question_text = updated_value
                    question.save()
                elif 'option_' in field_type:
                    option_index = int(field_type.split('_')[1])
                    options = question.options.all()
                    if option_index < len(options):
                        option = options[option_index]
                        option.option_text = updated_value
                        option.save()
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Invalid option index'})

                return JsonResponse({'status': 'success'})

            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid question index'})

        except Lesson.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Lesson not found'})
        except Quiz.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Quiz not found'})
        except Question.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Question not found'})
        except Option.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Option not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@csrf_exempt
def save_lesson_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            module_id = data.get('module_id')
            lesson_order = data.get('lesson_order')
            module = Module.objects.get(id=module_id)
            for lesson_data in lesson_order:
                lesson_id = lesson_data['id'].replace('lesson-', '')
                lesson = Lesson.objects.get(id=lesson_id, module=module)
                lesson.position = lesson_data['position']
                lesson.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
