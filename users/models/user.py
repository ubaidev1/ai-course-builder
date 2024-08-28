from django.contrib.auth.models import AbstractUser
from django.db import models

from users.manager import UserManager
from .base import BaseModel


class User(AbstractUser, BaseModel):
    """
    User model contains first_name, last_name, email and password
    """
    username = None
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        db_index=True,
        unique=True,
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
