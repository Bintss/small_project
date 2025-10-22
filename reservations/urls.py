# reservations/urls.py
from django.urls import path
from .views import AvailableSlotsView, ReservationCreateView, MyReservationListView

urlpatterns = [
    path('availability/', AvailableSlotsView.as_view(), name='available-slots'),
    path('', ReservationCreateView.as_view(), name='reservation-create'),
    path('my-reservations/', MyReservationListView.as_view(), name='my-reservations'),
]