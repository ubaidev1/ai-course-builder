from django.urls import path

from .views import *

urlpatterns = [
    path('home', home_view, name='home'),
    path('index/Course/<uuid:course_id>/', home_view, name='home'),
    path('next_lesson/<uuid:course_id>/', next_lesson_view, name='next_lesson'),

    path('retake_quiz/<uuid:course_id>/', retake_quiz, name='retake_quiz'),

    path('course/<uuid:course_id>/lesson/<uuid:lesson_id>/', course_detail_view, name='course_detail'),

    path('submit_quiz_score/<uuid:course_id>/<uuid:lesson_id>/', submit_quiz_score, name='submit_quiz_score'),
]
