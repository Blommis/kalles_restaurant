from uuid import UUID
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, date
from django.views.generic import ListView
from .models import Reservation
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings


# Create your views here.


def index(request):
    return render(request, 'booking/index.html')


@login_required(login_url='account_login')
def make_booking(request):
    """
    Handle table booking submission via POST request.

    **Process**

    - Retrieves form data: name, date, time, and number of guests.
    - Validates the date format; if invalid, returns an error message.
    - Checks how many bookings already exist for the selected date and time.
      If 3 or more bookings exist, the time slot is considered fully booked.
    - If valid, creates a new Reservation object and displays a success message
      including booking details and a unique booking reference.
    - If data is missing or an error occurs, displays a generic error message.

    **Redirects to:**

    :view:`booking:reservation_list`
    """
    if request.method == 'POST':
        input_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date_str = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date.')
            return redirect('booking:reservation_list')

        # max 3 bookings per time
        count = Reservation.objects.filter(date=date_obj, time=time).count()
        if count >= 3:
            messages.error(request,
                           f"Sorry, {time} on {date_str} is fully booked.")
            return redirect('booking:reservation_list')

        if time and guests:
            if input_name.strip():
                display_name = input_name.strip()
            else:
                display_name = (request.user.get_full_name() or request.user.username)

            reservation = Reservation.objects.create(
                user=request.user,
                name=display_name,
                email=email,
                phone=phone,
                date=date_obj,
                time=time,
                guests=guests
            )
            msg = (
                "Confirmed reservation:<br>"
                f"- Name: {display_name}<br>"
                f"- Email: {email}<br>"
                f"- Phone: {phone}<br>"
                f"- Date: {date_str}<br>"
                f"- Time: {time}<br>"
                f"- Guests: {guests}<br>"
                f"- Reference: <code>{reservation.booking_code}</code><br><br>"
                f"To see, change or cancel your reservation, visit "
                f"<a href='{reverse('booking:my_reservations')}' style='text-decoration: underline;'>My bookings</a>."
            )
            messages.success(request, msg, extra_tags="booking") 
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
        times_status = []

        if self.selected_date:
            try:
                selected_date_obj = datetime.strptime(
                    self.selected_date, '%Y-%m-%d'
                ).date()
            except ValueError:
                return []

            bookings = Reservation.objects.filter(
                date=selected_date_obj
                ).values('time').annotate(count=Count('booking_code'))
            booked_dict = {b['time'].strftime('%H:%M'): b['count'] for b in bookings}
            all_times = [
                '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00',
                '20:30', '21:00', '21:30', '22:00'
                ]
            for t in all_times:
                times_status.append({
                    "time": t,
                    "is_full": booked_dict.get(t, 0) >= 3
                })
        return times_status

    def get_context_data(self, **kwargs):
        """
        Add context data for reservation details.

        **Context**

        ``date``
        The selected date from the request's GET parameters.

        ``today``
        Today's date in ISO format.

        ``selected_date``
        The user-selected date.

        ``fully_booked_dates``
        List of fully booked dates.

        **Template:**
        :template:`booking/reservation_list.html`
        """
        context = super().get_context_data(**kwargs)
        today = date.today()
        context['date'] = self.request.GET.get('date', '')
        context['today'] = today.isoformat()
        context['selected_date'] = self.selected_date

        full_booked = Reservation.objects.values('date').annotate(
            count=Count('booking_code')
            ).filter(count__gte=3)
        context['fully_booked_dates'] = [
            res['date'].isoformat() for res in full_booked
            ]

        return context

@login_required(login_url='account_login')
def cancel_reservation(request):
    """
     Cancels a reservation based on the provided booking reference number.

    **POST Parameters:**
    - booking_code: The unique reference number for the reservation.

    - If the reservation exists, it is deleted and a success message is shown.
    - If not, an error message is displayed to the user.

    Redirects to the reservation list page after processing.
    """

    if request.method == 'POST':
        reservationnumber = request.POST.get('booking_code')
        try:
            UUID(reservationnumber)
        except ValueError:
            messages.error(request, "Invalid reference-id. Please try again.")
            return redirect('booking:my_reservations')

        try:
            reservation = Reservation.objects.get(
                booking_code=reservationnumber
            )
            if reservation.user_id != request.user.id:
                messages.error(request, "You can only cancel your own reservations.")
                return redirect('booking:my_reservations')
            
            reservation.delete()
            messages.success(request, "Reservation has been canceled", extra_tags="booking")
        except Reservation.DoesNotExist:
            messages.error(
                request,
                "No reservation were found with the reference number"
            )

        return redirect('booking:my_reservations')

@login_required(login_url='account_login')
def my_reservations(request):
    my_res = Reservation.objects.filter(user=request.user).order_by('date', 'time')
    return render(request, 'booking/my_reservations.html', {'reservations': my_res})


@login_required(login_url='account_login')
def update_reservation(request, booking_code):
    reservation = get_object_or_404(Reservation, booking_code=booking_code, user=request.user)

    bookings = Reservation.objects.filter(date=reservation.date).values('time').annotate(count=Count('booking_code'))
    booked_dict = {b['time'].strftime('%H:%M'): b['count'] for b in bookings}

    all_times = [
        '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00',
        '20:30', '21:00', '21:30', '22:00'
    ]
    reservation_time_str = reservation.time.strftime("%H:%M")
    available_times = [
        {
            "time": t,
            "count": booked_dict.get(t, 0),
            "is_full": booked_dict.get(t, 0) >= 3,
            "is_user_time": reservation_time_str == t
        }
        for t in all_times
    ]

    if request.method == 'POST':
        new_time = request.POST.get('time')
        new_date_str = request.POST.get('date')
        
        try:
            new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('booking:update_reservation', booking_code=booking_code)
        
        # block past dates
        if new_date < date.today():
            messages.error(request, "You cannot book a date in the past.")
            return redirect('booking:update_reservation', booking_code=booking_code)

        count = Reservation.objects.filter(date=new_date, time=new_time).exclude(booking_code=reservation.booking_code).count()
        if count >= 3:
            messages.error(request, f"Sorry, {new_time} on {new_date} is fully booked.")
            return redirect('booking:update_reservation', booking_code=booking_code)

        # update info
        reservation.name = request.POST.get('name')
        reservation.email = request.POST.get('email')
        reservation.phone = request.POST.get('phone')
        reservation.date = new_date
        reservation.time = new_time
        reservation.guests = request.POST.get('guests')
        reservation.save()

        messages.success(request, "Reservation updated!", extra_tags="booking")
        return redirect('booking:my_reservations')

    return render(request, 'booking/update_reservation.html', {
        'reservation': reservation,
        'available_times': available_times,
        'today': date.today().isoformat(),
    })


def test_email(request):
    subject = "Test from Kalles Restaurant"
    message = "Hi! This is a testmail"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["blomquist799@gmail.com"]

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse("Mail sent! check your inbox!")