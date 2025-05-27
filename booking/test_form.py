from django.test import TestCase
from booking.forms import ReservationForm
from datetime import date


class ReservationFormTests(TestCase):
    def test_form_valid_data(self):
        form_data = {
            'name': 'John Doe',
            'date': date.today().isoformat(),
            'time': '18:00',
            'guests': 4
        }
        form = ReservationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_missing_name(self):
        form_data = {
            'name': '',
            'date': date.today().isoformat(),
            'time': '18:00',
            'guests': 4
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_invalid_guests(self):
        form_data = {
            'name': 'Jane',
            'date': date.today().isoformat(),
            'time': '19:00',
            'guests': ''  
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('guests', form.errors)
