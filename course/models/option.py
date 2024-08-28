from django.db import models

from course.models.question import Question
from users.models import BaseModel


class Option(BaseModel):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text
