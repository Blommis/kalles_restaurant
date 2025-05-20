from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Reservation


# Register your models here.
@admin.register(Reservation)

class bookingAdmin(SummernoteModelAdmin):
    list_display = ('name', 'date', 'time', 'guests')
    search_fields = ['name', 'date', 'time']
    list_filter = ('date', 'time', 'guests')
