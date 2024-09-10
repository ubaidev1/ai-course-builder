import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from course.models import Course, Module, Lesson, Quiz, Question, Option


@csrf_exempt
def update_course(request, course_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            course_data = data

            # Get the course by ID
            course = Course.objects.get(id=course_id)
            course.title = course_data['course_name']
            course.description = course_data['course_description']
            course.save()

            # Update modules
            for module_data in course_data['modules']:
                module_title = module_data['module_title']
                module, created = Module.objects.get_or_create(course=course, title=module_title)

                # Update module details
                module.title = module_data['module_title']
                module.description = module_data['module_description']
                module.save()

                # Update lessons
                for lesson_data in module_data['module_lessons']:
                    lesson_title = lesson_data['lesson_title']
                    lesson, created = Lesson.objects.get_or_create(module=module, title=lesson_title)

                    # Update lesson details
                    lesson.title = lesson_data['lesson_title']
                    lesson.content = lesson_data['lesson_content']
                    lesson.save()

                    # Update quizzes
                    for quiz_data in lesson_data['quiz']:
                        quiz_title = quiz_data['title']
                        quiz, created = Quiz.objects.get_or_create(lesson=lesson, title=quiz_title)

                        # Update quiz details
                        quiz.title = quiz_data['title']
                        quiz.save()

                        # Update questions
                        for question_data in quiz_data['questions']:
                            question_text = question_data['question']
                            question, created = Question.objects.get_or_create(quiz=quiz, question_text=question_text)

                            # Update question details
                            question.question_text = question_data['question']
                            question.correct_answer = question_data['correct_answer']
                            question.save()

                            # Update options
                            for option_text in question_data['options']:
                                option, created = Option.objects.get_or_create(question=question,
                                                                               option_text=option_text)
                                option.option_text = option_text
                                option.save()

            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
