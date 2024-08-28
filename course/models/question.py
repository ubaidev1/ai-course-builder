from django.db import models

from course.models.quiz import Quiz
from users.models import BaseModel


class Question(BaseModel):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text
