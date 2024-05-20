from django.utils import timezone

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from All_models.models import LobType, Lobby, Wedding
from .serializers import LobTypeSerializer, LobbySerializers, CustomLobbySerializers


# ##################### LOBBY TYPE ##################### #


# Get Lob Type
class LobTypeViews(generics.ListAPIView):
    queryset = LobType.objects.filter(deleted_at=None)
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


# ##################### LOBBY  ##################### #


# Get Lobby
class LobbyViews(generics.ListAPIView):
    queryset = Lobby.objects.all()
    serializer_class = CustomLobbySerializers

    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request
        date = request.query_params.get('date')
        if date:
            filtered_weddings = Wedding.objects.filter(wedding_date=date)
            context['filtered_weddings'] = filtered_weddings
        return context





