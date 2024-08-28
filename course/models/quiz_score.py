from django.db import models

from course.models import Quiz
from users.models import BaseModel, User


class QuizScore(BaseModel):
    user = models.ForeignKey(User, related_name='quiz_scores', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='user_scores', on_delete=models.CASCADE)
    score = models.IntegerField()


