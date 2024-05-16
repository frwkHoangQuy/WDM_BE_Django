from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name="Register"),
    path('auth/login/', views.LoginView.as_view(), name="Login"),
    path('auth/verify-token/', views.verify_token, name="Verify Token")
]
