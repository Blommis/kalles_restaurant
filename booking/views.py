from django.shortcuts import render, redirect
from datetime import datetime
from django.http import HttpResponse 
from django.views.generic import ListView
from .models import Reservation
from .forms import ReservationForm
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'booking/index.html')


def make_booking(request):
   
    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')

        if name and date and time and guests:
            Reservation.objects.create(
                name=name,
                date=date,
                time=time,
                guests=guests
            )
            messages.success(request, f"For {name} on {date} at {time} for {guests} guests.")
            return redirect('booking:reservation_list')
    
    messages.error(request, 'something went wrong, please try again')
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
        
        date = self.request.GET.get('date')
        available_times = []

        if date: 
            try:
                selected_date = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                return HttpResponse("Invalid date format.", status=400)
            
            booked_times = Reservation.objects.filter(date=selected_date).values_list('time', flat=True)
            all_times = ['17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00' ]
            available_times = [time for time in all_times if time not in booked_times] 
        
        return available_times


