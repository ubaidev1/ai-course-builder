from django.db import models

from users.models import BaseModel


class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1500, null=True, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
