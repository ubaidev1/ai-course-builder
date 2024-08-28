import json
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404

from antropic_api.anthropic_response import get_ai_course_details
from course.models import Course
from scripts.create_course import create_course
from scripts.extend_existing_course import extend_existing_course
from users.models import User


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
            messages.error(request, 'An account with this email already exists.')
        else:
            User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            messages.success(request, 'Account created successfully! Please log in.')
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
def dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    try:
        if request.method == 'POST' and request.FILES.get('pdf_file'):
            pdf_file = request.FILES['pdf_file']
            fs = FileSystemStorage(location='/tmp')
            filename = fs.save(pdf_file.name, pdf_file)
            pdf_file_path = fs.path(filename)

            json_data = get_ai_course_details('config.json', pdf_file_path)
            data = json.loads(json_data)
            create_course(data)
            os.remove(pdf_file_path)
        courses = Course.objects.all()
        return render(request, 'dashboard.html', {'courses': courses})

    except Exception as e:
        return render(request, 'dashboard.html', {
            'courses': Course.objects.all(),
            'error_message': f"An unexpected error occurred: {str(e)}"
        })


@login_required
def extend_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        pdf_file = request.FILES.get('pdf_file')
        if not course_id or not pdf_file:
            messages.error(request, "Please select a course and upload a PDF file.")
            return redirect('dashboard')
        course = get_object_or_404(Course, id=course_id)
        fs = FileSystemStorage(location='/tmp')
        filename = fs.save(pdf_file.name, pdf_file)
        pdf_file_path = fs.path(filename)
        json_data = get_ai_course_details('config.json', pdf_file_path)
        data = json.loads(json_data)
        extend_existing_course(data, course)
    courses = Course.objects.all()
    return render(request, 'dashboard.html', {'courses': courses})
