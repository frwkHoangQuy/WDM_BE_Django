from django.contrib import admin
from django.urls import path, include
from .views import LobbyTypeViews


urlpatterns = [
    path('lobby/types/', LobbyTypeViews.as_view(), name="get_lobby_type"),
]
