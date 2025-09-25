from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Reservation


# Register your models here.
@admin.register(Reservation)
class ReservationAdmin (SummernoteModelAdmin):
    list_display = ('user', 'booking_code', 'name', 'email', 'phone', 'date', 'time', 'guests')
    search_fields = ['user', 'booking_code', 'name', 'email', 'phone', 'date', 'time']
    list_filter = ('date', 'time', 'guests')
