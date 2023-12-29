"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


app_name = 'user'


# Define URL patterns for user-related views
urlpatterns = [
    # Endpoint for creating a new user
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
