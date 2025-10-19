# users/urls.py
from django.urls import path
from .views import UserSignupView, MyProfileView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('me/', MyProfileView.as_view(), name='my-profile'),
]