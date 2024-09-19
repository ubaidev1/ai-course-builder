from users.models.user import User
from django.db import models
from users.models import BaseModel


class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1500, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title
