from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('delete/user/<str:username>/', views.DeleteUserByUsernameView.as_view()),
    path('auth/register/', views.RegisterView.as_view(), name="Register"),
    path('auth/login/', views.LoginView.as_view(), name="Authentication"),
]
