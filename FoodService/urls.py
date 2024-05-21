from django.contrib import admin
from django.urls import path, include
from .food_views import FoodViews, FoodCreateViews, FoodEditViews, FoodSoftDeleteViews
from .service_view import ServiceViews, ServiceCreateViews, ServiceEditViews, ServiceSoftDeleteViews

food_urls = [
    path('food/create/', FoodCreateViews.as_view(), name="create_food"),
    path('food/delete/<str:id>/', FoodSoftDeleteViews.as_view(), name="soft_delete_food"),
    path('food/<str:id>/', FoodEditViews.as_view(), name="edit_food"),
    path('food/', FoodViews.as_view(), name="get_food"),
]

service_urls = [
    path('service/create/', ServiceCreateViews.as_view(), name="create_service"),
    path('service/delete/<str:id>/', ServiceSoftDeleteViews.as_view(), name="soft_delete_service"),
    path('service/<str:id>/', ServiceEditViews.as_view(), name="edit_service"),
    path('service/', ServiceViews.as_view(), name="get_service"),
]

urlpatterns = [] + food_urls + service_urls
