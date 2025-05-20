from django.urls import path # import path, similar to project's urls.py
from .views import ReservationListView, index # import views.py from the currentdirectory

urlpatterns = [ path('', index, name='index'),
                path('reservations/', ReservationListView.as_view(), name='reservation_list'),] 
