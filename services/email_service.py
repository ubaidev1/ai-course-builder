from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class EmailServices:
    """
    Email service to send email verification link to the user
    """

    @staticmethod
    def send_email_to_client(user, email, invitation_link, template_name='invitation_email.html',
                             subject="Course Invitation Link", ):

        kwargs = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'invitation_link': invitation_link
        }
        message = render_to_string(template_name, kwargs)

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list, html_message=message)
        except Exception as e:
            print(e)
