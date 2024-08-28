from django.urls import path

from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('result/', result_view, name='result'),
    path('extend_course/', extend_course, name='extend_course'),
    path('', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
