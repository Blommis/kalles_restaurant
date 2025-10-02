from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # only when new user creates
        subject = "Welcome to Kalle's Restaurant!"
        message = (
            f"Hi {instance.username}"
            "Thank you for signing up at Kalle's Restaurant!"
            "You can now manage your bookings, update details, and never miss your table."
            "We look forward to seeing you soon!"
            "Best regards,"
            "Kalle's team"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [instance.email])
