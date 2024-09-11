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

            # Retrieve the course by course_id
            try:
                course = Course.objects.get(id=course_id)
                course.title = course_data['course_name']
                course.description = course_data['course_description']
                course.save()  # Save course changes if any
            except Course.DoesNotExist:
                return JsonResponse({'error': 'Course not found'}, status=404)

            # Process modules
            for module_data in course_data.get('modules', []):
                try:
                    module = Module.objects.get(id=module_data['module_id'], course=course)
                    module.title = module_data['module_title']
                    module.save()
                except Module.DoesNotExist:
                    module = Module.objects.create(
                        id=module_data['module_id'],
                        course=course,
                        title=module_data['module_title']
                    )

                # Process lessons
                for lesson_data in module_data.get('module_lessons', []):
                    try:
                        lesson = Lesson.objects.get(id=lesson_data['lesson_id'], module=module)
                        lesson.title = lesson_data['lesson_title']
                        lesson.content = lesson_data['lesson_content']
                        lesson.save()
                    except Lesson.DoesNotExist:
                        lesson = Lesson.objects.create(
                            id=lesson_data['lesson_id'],
                            module=module,
                            title=lesson_data['lesson_title'],
                            content=lesson_data['lesson_content']
                        )

                    # Process quizzes
                    for quiz_data in lesson_data.get('quizzes', []):
                        try:
                            quiz = Quiz.objects.get(id=quiz_data['quiz_id'], lesson=lesson)
                            quiz.title = quiz_data['quiz_title']
                            quiz.save()
                        except Quiz.DoesNotExist:
                            quiz = Quiz.objects.create(
                                id=quiz_data['quiz_id'],
                                lesson=lesson,
                                title=quiz_data['quiz_title']
                            )

                        # Process questions
                        for question_data in quiz_data.get('questions', []):
                            try:
                                question = Question.objects.get(id=question_data['question_id'], quiz=quiz)
                                question.question_text = question_data['question_text']
                                question.correct_answer = question_data['correct_answer']
                                question.save()
                            except Question.DoesNotExist:
                                question = Question.objects.create(
                                    id=question_data['question_id'],
                                    quiz=quiz,
                                    question_text=question_data['question_text'],
                                    correct_answer=question_data['correct_answer']
                                )

                            # Process options
                            for option_data in question_data.get('options', []):
                                try:
                                    option = Option.objects.get(id=option_data['option_id'], question=question)
                                    option.option_text = option_data['option_text']
                                    option.save()
                                except Option.DoesNotExist:
                                    Option.objects.create(
                                        id=option_data['option_id'],
                                        question=question,
                                        option_text=option_data['option_text']
                                    )

            return JsonResponse({'message': 'Course updated successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
