from course.models.course import Course
from django.db import models
from users.models import BaseModel


class Module(BaseModel):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1500, null=True, blank=True)

    def __str__(self):
        return self.title
