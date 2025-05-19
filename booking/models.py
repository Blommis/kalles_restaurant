from django.db import models 
# Create your models here.


class booking(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()


