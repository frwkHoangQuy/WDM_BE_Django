from django.contrib import admin
from django.urls import path, include
from .views import (LobTypeViews, LobTypeUpdateViews, LobTypeSoftDeleteViews,
                    LobTypeCreateViews, LobbyViews, LobbyCreateView)


urlpatterns = [
    path('lobby/type/<str:id>/soft-delete/', LobTypeSoftDeleteViews.as_view(), name='lob_type_soft_delete'),
    path('lobby/type/<str:id>/update/', LobTypeUpdateViews.as_view(), name='lob_type_update'),
    path('lobby/type/create/', LobTypeCreateViews.as_view(), name='create_lob_type'),
    path('lobby/types/', LobTypeViews.as_view(), name="get_lobby_type"),
    path('lobby/create/', LobbyCreateView.as_view(), name='create_lobby'),
    path('lobby/', LobbyViews.as_view(), name='get_lobby')
]
