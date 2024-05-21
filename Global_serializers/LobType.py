from rest_framework import serializers
from All_models.models import LobType


class LobTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LobType
        fields = '__all__'
