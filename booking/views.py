from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse 
from django.views.generic import ListView
from .models import Reservation
from .forms import ReservationForm

# Create your views here.

def index(request):
    return render(request, 'booking/index.html')

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


