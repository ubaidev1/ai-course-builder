from course.models.module import Module
from django.db import models
from users.models import BaseModel


class Lesson(BaseModel):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title
