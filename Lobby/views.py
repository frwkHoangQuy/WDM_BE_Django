from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.shortcuts import get_list_or_404
from django.utils.dateparse import parse_datetime

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from All_models.models import LobType, Lobby, Wedding
from Global_serializers.LobType import LobTypeSerializer
from Global_serializers.Lobby import LobbySerializers
from .serializers import CustomLobbySerializers
from Authentication.Middleware.jwt_authentication import  PermissionRequiredMixin


class LobbyAccessPermission(PermissionRequiredMixin):
    permission_required = 'Access Lobby'

# ##################### LOBBY TYPE ##################### #


# Get Lob Type
class LobTypeViews(LobbyAccessPermission, generics.ListAPIView):
    queryset = LobType.objects.except_soft_delete()
    serializer_class = LobTypeSerializer


# Update Lob Type
class LobTypeUpdateViews(LobbyAccessPermission, generics.UpdateAPIView):
    queryset = LobType.objects.all()
    serializer_class = LobTypeSerializer
    lookup_field = 'id'


# Create LobType
class LobTypeCreateViews(LobbyAccessPermission, generics.CreateAPIView):
    queryset = LobType.objects.all()
    serializer_class = LobTypeSerializer


# Soft Delete Lob Type
class LobTypeSoftDeleteViews(LobbyAccessPermission, generics.UpdateAPIView):
    queryset = LobType.objects.all()
    serializer_class = LobTypeSerializer
    lookup_field = 'id'

    def partial_update(self, request, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ##################### LOBBY  ##################### #


# Get Lobby
class LobbyViews(LobbyAccessPermission, generics.ListAPIView):
    serializer_class = CustomLobbySerializers

    def get_queryset(self):
        queryset = Lobby.objects.except_soft_delete()
        lobby_id = self.request.query_params.get('lob_type_id')
        if lobby_id is not None:
            queryset = queryset.filter(lob_type_id=lobby_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        date = self.request.query_params.get('date')
        if date:
            filtered_weddings = Wedding.objects.filter(wedding_date=date)
            context['filtered_weddings'] = filtered_weddings
        else:
            context['filtered_weddings'] = Wedding.objects.none()
        return context


class LobbyCreateView(LobbyAccessPermission, generics.CreateAPIView):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializers


class LobbyUpdateView(LobbyAccessPermission, generics.UpdateAPIView):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializers
    lookup_field = 'id'


class LobbyDeleteView(LobbyAccessPermission, APIView):
    def patch(self, request, id):
        try:
            soft_delete_lobby = Lobby.objects.get(id=id)
            soft_delete_lobby.soft_delete()
            return Response({"detail": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"detail": "Không tìm thấy Lobby cần xóa"}, status=status.HTTP_404_NOT_FOUND)
