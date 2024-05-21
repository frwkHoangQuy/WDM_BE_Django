from django.contrib import admin
from django.urls import path, include
from .views import FoodViews

urlpatterns = [
    path('food/', FoodViews.as_view(), name="get_food")
]
