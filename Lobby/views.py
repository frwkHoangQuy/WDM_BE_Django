from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from All_models.models import LobType, Lobby, Wedding
from Global_serializers.LobType import LobTypeSerializer
from Global_serializers.Lobby import LobbySerializers
from .serializers import CustomLobbySerializers


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
    serializer_class = CustomLobbySerializers

    def get_queryset(self):
        lob_type_id = self.request.query_params.get('lob_type_id')
        if id is not None:
            queryset = Lobby.objects.all().filter(lob_type_id=lob_type_id, deleted_at=None)
        else:
            queryset = {}
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        request = self.request
        date = request.query_params.get('date')
        if date:
            filtered_weddings = Wedding.objects.filter(wedding_date=date)
            context['filtered_weddings'] = filtered_weddings
        return context


class LobbyCreateView(generics.CreateAPIView):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializers


@api_view(['PATCH'])
def LobbyDeleteView(request, id):
    try:
        soft_delete_lobby = Lobby.objects.get(id=id)
        soft_delete_lobby.deleted_at = timezone.now()
        soft_delete_lobby.save()
        return Response({"detail": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({"detail": "Không tìm thấy Lobby cần xóa"}, status=status.HTTP_404_NOT_FOUND)








