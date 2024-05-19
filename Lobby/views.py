from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics


from .models import LobType, Lobby
from .serializers import LobTypeSerializer


class LobbyTypeViews(generics.ListAPIView):
    queryset = LobType.objects.all()
    serializer_class = LobTypeSerializer
