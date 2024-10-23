# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .tasks import send_mail


@receiver(post_save, sender=CustomUser)
def send_mail_signal(sender, instance, created, **kwargs):
    if instance.otp:
        send_mail.delay(instance.id)
