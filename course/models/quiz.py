from django.db import models

from users.models import BaseModel
from course.models.lesson import Lesson


class Quiz(BaseModel):
    title = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
