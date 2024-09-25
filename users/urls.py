from django.urls import path
from scripts.update_course import update_course

from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('edit_course/<uuid:course_id>/', edit_course, name='edit_course'),
    path('course_actions/', course_actions, name="course_actions"),
    path('toggle-course-publish/<uuid:course_id>/', toggle_course_publish, name='toggle_course_publish'),
    path('update-course/<uuid:course_id>/', update_course, name='update_course'),
    path('delete-course/<uuid:course_id>/', delete_course, name='delete_course'),
    path('result/', result_view, name='result'),
    path('send-invite/<uuid:course_id>/', send_invite, name='send_invite'),
    path('enroll_course/<uuid:course_id>/', enroll_course, name='enroll_course'),
    path('extend_course/<uuid:course_id>/', extend_course, name='extend_course'),
    path('customize/', customize_color, name='customize_color'),
    path('', signup, name='signup'),
    path('admin_signup', admin_signup, name='admin_signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
