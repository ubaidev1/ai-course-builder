from course.models.lesson import Lesson
from django.db import models
from users.models import BaseModel


class Video(BaseModel):
    video_link = models.URLField()
    lesson = models.OneToOneField(Lesson, related_name='video', on_delete=models.CASCADE)

    def __str__(self):
        return self.video_link
