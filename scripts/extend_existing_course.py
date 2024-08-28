from course.models import Module, Lesson, Quiz, Question, Option


def extend_existing_course(data, course):
    for module_data in data.get('modules', []):
        module_title = module_data.get('module_title')
        module_description = module_data.get('module_description', '')

        module = Module.objects.create(
            course=course,
            title=module_title,
            description=module_description,
        )

        for lesson_data in module_data.get('module_lessons', []):
            lesson_title = lesson_data.get('lesson_title')
            lesson_content = lesson_data.get('lesson_content')

            lesson = Lesson.objects.create(
                module=module,
                title=lesson_title,
                content=lesson_content,
            )

            if 'quiz' in lesson_data:
                quiz_title = f"Quiz for {lesson_title}"
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    title=quiz_title,
                )
                for question_data in lesson_data.get('quiz', []):
                    question_text = question_data.get('question')
                    correct_answer = question_data.get('correct_answer')

                    question = Question.objects.create(
                        quiz=quiz,
                        question_text=question_text,
                        correct_answer=correct_answer,
                    )

                    for option_text in question_data.get('options', []):
                        Option.objects.create(
                            question=question,
                            option_text=option_text,
                        )

    print("Course content updated successfully!")
