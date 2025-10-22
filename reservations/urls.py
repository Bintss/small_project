# reservations/urls.py
from django.urls import path
from .views import AvailableSlotsView, ReservationCreateView

urlpatterns = [
    path('availability/', AvailableSlotsView.as_view(), name='available-slots'),
    path('', ReservationCreateView.as_view(), name='reservation-create'),
]