from django.contrib import admin
from django.urls import path, include
from .views import FoodViews, FoodCreateViews, FoodEditViews, FoodSoftDeleteViews

urlpatterns = [
    path('food/create/', FoodCreateViews.as_view(), name="create_food"),
    path('food/delete/<str:id>/', FoodSoftDeleteViews.as_view(), name="edit_food"),
    path('food/<str:id>/', FoodEditViews.as_view(), name="edit_food"),
    path('food/', FoodViews.as_view(), name="get_food"),
]
