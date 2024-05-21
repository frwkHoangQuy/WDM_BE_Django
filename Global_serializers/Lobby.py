from rest_framework import serializers
from All_models.models import Lobby


class LobbySerializers(serializers.ModelSerializer):

    class Meta:
        model = Lobby
        fields = '__all__'
