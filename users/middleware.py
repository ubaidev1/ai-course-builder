from course.models import CourseEnrollment
from users.models import CustomizationSettings


class CustomizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_admin:
                customization_settings = CustomizationSettings.objects.filter(admin=request.user).first()
                request.customization_settings = customization_settings
            enrollment = CourseEnrollment.objects.filter(user=request.user).first()
            if enrollment:
                customization_settings = CustomizationSettings.objects.filter(admin=enrollment.invited_by).first()
                request.customization_settings = customization_settings
            else:
                request.customization_settings = None
        else:
            request.customization_settings = None

        response = self.get_response(request)
        return response
