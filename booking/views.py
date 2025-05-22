from django.shortcuts import render, redirect
from datetime import datetime, date
from django.http import HttpResponse 
from django.views.generic import ListView
from .models import Reservation
from .forms import ReservationForm
from django.contrib import messages
from django.db.models import Count 
# Create your views here.


def index(request):
    return render(request, 'booking/index.html')


def make_booking(request):
    if request.method == 'POST':
        booking_code = request.POST.get('booking_code')
        name = request.POST.get('name')
        date_str = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date.')
            return redirect('booking:reservation_list')

        # Kontrollera antal bokningar för det datum + tid
        count = Reservation.objects.filter(date=date_obj, time=time).count()
        if count >= 3:
            messages.error(request, f"Sorry, {time} on {date_str} is fully booked.")
            return redirect('booking:reservation_list')

        if name and time and guests:
            reservation = Reservation.objects.create(
                name=name,
                date=date_obj,
                time=time,
                guests=guests
            )
            messages.success(request, f"For {name} on {date_str} at {time} for {guests} guests. Your booking reference is: {reservation.booking_code}")
            return redirect('booking:reservation_list')

    messages.error(request, 'Something went wrong, please try again.')
    return redirect('booking:reservation_list')


class ReservationListView(ListView):
    model = Reservation
    template_name = 'booking/reservation_list.html'
    context_object_name = 'reservations'
    
    def get_queryset(self):
        """
    Display available reservation times for a selected date.

    **Context**

    ``available_times``
    A list of time slots (strings) that are not yet booked on the given date.

    **Template:**

    :template:`booking/reservation_list.html`
    """
        
        self.selected_date = self.request.GET.get('date')
        available_times = []

        if self.selected_date:
            try:
                selected_date_obj = datetime.strptime(self.selected_date, '%Y-%m-%d').date()
            except ValueError:
                return []
            
            booked_times = Reservation.objects.filter(date=selected_date_obj).values_list('time', flat=True)
            all_times = ['17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00']
            available_times = [time for time in all_times if time not in booked_times]
        
        return available_times
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        context['date'] = self.request.GET.get('date', '')
        context['today'] = today.isoformat()
        context['selected_date'] = self.selected_date

        full_booked = Reservation.objects.values('date').annotate(count=Count('booking_code')).filter(count__gte=3)
        context['fully_booked_dates'] = [res['date'].isoformat() for res in full_booked]

        return context


def cancel_reservation(request):
    if request.method == 'POST':
        reservationnumber = request.POST.get('booking_code')
        try:
            reservation = Reservation.objects.get(booking_code=reservationnumber)
            reservation.delete()
            messages.success(request, "Reservation has been canceled")
        except Reservation.DoesNotExist:
            messages.error(request, "No reservation were found with the reference number")

        return redirect('booking:reservation_list')