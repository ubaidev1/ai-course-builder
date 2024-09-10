from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('course_actions/', course_actions, name="course_actions"),
    path('toggle-course-publish/<uuid:course_id>/', toggle_course_publish, name='toggle_course_publish'),
    path('result/', result_view, name='result'),
    path('invite-users/', invite_user, name='invite_user'),
    path('send-invite/<uuid:course_id>/', send_invite, name='send_invite'),
    path('accept_invitation/<str:token>/', accept_invitation, name='accept_invitation'),
    path('extend_course/', extend_course, name='extend_course'),
    path('', signup, name='signup'),
    path('admin_signup', admin_signup, name='admin_signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
