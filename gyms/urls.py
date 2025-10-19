# gyms/urls.py
from django.urls import path
from .views import GymCreateView

urlpatterns = [
    path('', GymCreateView.as_view(), name='gym-create'),
]