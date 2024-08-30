from django.urls import path

from .views import *

urlpatterns = [
    path('home/', home_view, name='home'),
    path('course/<uuid:course_id>/', course_detail_view, name='course_detail'),
    path('course/<uuid:course_id>/lesson/<uuid:lesson_id>/', course_detail_view,
         name='lesson_detail'),
    path('submit_quiz_score/<uuid:lesson_id>/', submit_quiz_score, name='submit_quiz_score'),
]
