from django.db import models
from users.models.base import BaseModel
from users.models.user import User


class CustomizationSettings(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    heading_color = models.CharField(max_length=7, blank=True, null=True)
    navbar_color = models.CharField(max_length=7, default='#000000')
    button_color = models.CharField(max_length=7, blank=True, null=True)
    background_color = models.CharField(max_length=7, blank=True, null=True)
    points_color = models.CharField(max_length=7, blank=True, null=True)
