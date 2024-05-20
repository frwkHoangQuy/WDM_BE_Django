from rest_framework import serializers
from .models import LobType


class LobTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LobType
        fields = '__all__'
