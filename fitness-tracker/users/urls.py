from django.urls import path
from .views import UserRegistrationView, UserProfileView

urlpatterns = [
    path('users/register/', UserRegistrationView.as_view(), name='register'),
    path('users/profile/', UserProfileView.as_view(), name='profile'),
]