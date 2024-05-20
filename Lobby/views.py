from django.shortcuts import get_list_or_404
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from .models import LobType, Lobby
from .serializers import LobTypeSerializer


# Get Lob Type
class LobTypeViews(generics.ListAPIView):
    queryset = LobType.objects.all()
    serializer_class = LobTypeSerializer


# Update Lob Type
class LobTypeUpdateViews(generics.UpdateAPIView):
    queryset = LobType.objects.all()
    serializer_class = LobTypeSerializer
    lookup_field = 'id'


# Create LobType
class LobTypeCreateViews(generics.CreateAPIView):
    queryset = LobType.objects.all()
    serializer_class = LobTypeSerializer


# Soft Delete Lob Type
class LobTypeSoftDeleteViews(generics.UpdateAPIView):
    queryset = LobType.objects.all()
    serializer_class = LobTypeSerializer
    lookup_field = 'id'

    def partial_update(self, request, **kwargs):
        instance = self.get_object()
        instance.deleted_at = timezone.now()
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
