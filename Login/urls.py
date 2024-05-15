from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('delete/user/<str:username>/', views.DeleteUserByUsernameView.as_view()),
    path('register/', views.RegisterView.as_view(), name="Register"),
    path('login/', views.LoginView.as_view(), name="Login"),

]
