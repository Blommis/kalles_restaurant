from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Reservation


# Register your models here.
@admin.register(Reservation)
class ReservationAdmin (SummernoteModelAdmin):
    list_display = ('booking_code', 'name', 'date', 'time', 'guests')
    search_fields = ['booking_code', 'name', 'date', 'time']
    list_filter = ('date', 'time', 'guests')