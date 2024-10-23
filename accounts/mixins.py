from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


class SendEamilMixin:
    email_template = ''

    def send_email(self, subject, recipient):
        context = self.get_email_context()
        email_template = self.get_email_template()

        print(email_template)
        print(context)
        html_message = render_to_string(template_name=email_template, context=context)
        message = strip_tags(html_message)
    
        return send_mail(
                subject=subject,
                from_email=settings,
                recipient_list=[recipient],
                message=message,
                html_message=html_message
        )

    def get_email_context(self):
        return {
            'view': self
        }
    
    def get_email_template(self):
        return self.email_template


