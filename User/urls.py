from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('users/<str:username>/delete/', views.DeleteUserByUsernameView.as_view(), name="Delete"),
    path('users/', views.UsersViews.as_view(), name="Users")
]
