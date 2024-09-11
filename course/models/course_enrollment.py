from django.db import models

from course.models.course import Course
from coursebuilder import settings
from users.models import BaseModel
from users.models.user import User


class CourseEnrollment(BaseModel):
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enrollments', )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollment')
