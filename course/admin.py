from django.contrib import admin

from course.models import *

# Register your models here.

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(QuizScore)
