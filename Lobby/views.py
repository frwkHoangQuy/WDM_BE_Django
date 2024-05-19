from django.shortcuts import get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import LobType, Lobby
from .serializers import LobTypeSerializer


class LobbyPageViews(APIView):

    def get(self, request):
        pass


class LobbyTypeViews(LobbyPageViews):

    def get(self, request):
        lob_types = get_list_or_404(LobType)
        serializer = LobTypeSerializer(lob_types, many=True)
        return Response(serializer.data)
