from django.db import models 
import uuid
# Create your models here.


class Reservation(models.Model):
    booking_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()


