from django.contrib import admin
from django.urls import path, include
from .views import WeddingListView, WeddingCreateView

urlpatterns = [
    path('wedding/create/wedding/', WeddingCreateView.as_view(), name='create_wedding'),
    path('wedding/', WeddingListView.as_view(), name='get_wedding'),
]
