from django.db import models
from django.conf import settings
import uuid
# Create your models here.


class Reservation(models.Model):
    booking_code = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models. ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations',
        null=True, blank=True
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
