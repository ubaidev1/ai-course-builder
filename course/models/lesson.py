from django.db import models

from course.models.module import Module
from users.models import BaseModel


class Lesson(BaseModel):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
