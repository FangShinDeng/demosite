from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from datetime import datetime
from .utils import token_generator
import threading

class EmailThread(threading.Thread):
    def __init__(self, email) -> None:
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()

def custom_send_mail(subject:str, receivers:list, html_template:str, context:dict) -> None:

    # email_template = render_to_string(template_name=html_template,context=context)
    message = get_template(template_name=html_template).render(context)
    email = EmailMessage(
        subject,  # 電子郵件標題
        message,  # 電子郵件內容
        settings.EMAIL_HOST_USER,  # 寄件者
        receivers  # 收件者
    )
    email.fail_silently = False
    email.content_subtype = "html"
    # email.send()
    EmailThread(email).start()

def send_activate_mail(request, user) -> None:

    context = {
        "username": user.username, 
        "domain": get_current_site(request),
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": token_generator.make_token(user),
    }
    custom_send_mail(
        subject="Register Success Inform", 
        receivers=[user.email],
        html_template="emails/email_activate.html",
        context=context
        )
    