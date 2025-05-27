from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from datetime import datetime
from .models import Reservation


class BookingTests(TestCase):
    def setUp(self):
        """
        Set up initial data for testing.
        """
        self.url_reservation_list = reverse('booking:reservation_list')
        self.url_make_booking = reverse('booking:make_booking')
        self.url_cancel_reservation = reverse('booking:cancel_reservation')

    def test_make_booking_valid(self):
        """
        Test making a valid booking.
        """
        # make a POST request to create a reservtion
        response = self.client.post(self.url_make_booking, {
            'name': 'John Doe',
            'date': '2025-05-30',
            'time': '19:00',
            'guests': 4,
        })

        # checks if the message is correct
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            "For John Doe on 2025-05-30 at 19:00 for 4 guests." in str(m)
            for m in messages))
        # Checks if booking references appplys in the message
        found = any("Your booking reference is:" in str(m) for m in messages)
        self.assertTrue(found)

    def test_make_booking_invalid_date(self):
        """
        Test making a booking with invalid date.
        """
        response = self.client.post(self.url_make_booking, {
            'name': 'Jane Doe',
            'date': 'invalid-date',
            'time': '19:00',
            'guests': 2,
        })
        # Check if there was a redirect
        self.assertRedirects(response, self.url_reservation_list)

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Invalid date.')

    def test_cancel_reservation_success(self):
        """
        Test canceling a reservation.
        """
        reservation = Reservation.objects.create(
            name='Jane Doe',
            date=datetime.strptime('2025-05-30', '%Y-%m-%d').date(),
            time='19:00',
            guests=2
        )

        response = self.client.post(self.url_cancel_reservation, {
            'booking_code': reservation.booking_code
        })

        # Check if the reservation is deleted and redirected
        self.assertRedirects(response, self.url_reservation_list)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Reservation has been canceled")

        # Check if the reservation is actually deleted
        with self.assertRaises(Reservation.DoesNotExist):
            Reservation.objects.get(booking_code=reservation.booking_code)

    def test_cancel_reservation_invalid_code(self):
        """
        Test canceling a reservation with an invalid booking code.
        """
        response = self.client.post(self.url_cancel_reservation, {
            'booking_code': 'f1d6c98d-72d9-4f56-b321-99682ba7f068'
        })

        # Check if there was a redirect
        self.assertRedirects(response, self.url_reservation_list)

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]),
                         "No reservation were found with the reference number")
