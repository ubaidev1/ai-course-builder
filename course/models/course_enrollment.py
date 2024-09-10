from django.db import models

from course.models.course import Course
from users.models import BaseModel
from users.models.user import User


class CourseEnrollment(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollment')
