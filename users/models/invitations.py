from django.db import models

from course.models import Course
from users.models.base import BaseModel
from users.models.user import User


class UserInvitation(BaseModel):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
    ]
    admin = models.ForeignKey(User, related_name='invitations', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
