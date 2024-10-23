from celery import shared_task
import celery.exceptions
from django.core.mail import EmailMessage
from .models import CustomUser as User
import os
import celery

@shared_task
def send_mail(user_id):
    user = User.objects.filter(id=user_id).first()
    if user:
        message = f"Your account verification otp is {user.otp}"
        mail = EmailMessage(
            subject="Account Verification",
            body=message,
            from_email=os.getenv("EMAIL_HOST_USER"),
            to=[user.email],
        )
        mail.send()
        return "mail sent"
    else:
        raise ValueError("Invalid user")
  