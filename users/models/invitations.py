from django.db import models

from course.models import Course
from users.models import BaseModel


class UserInvitation(BaseModel):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
    ]
    email = models.EmailField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='invitations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
