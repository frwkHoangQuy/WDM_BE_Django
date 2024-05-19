from rest_framework import serializers
from .models import LobType


class LobTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LobType
        fields = '__all__'


class LobTypeUpdateSerializer(serializers.ModelSerializer):
    max_table_count = serializers.IntegerField(required=False)
    min_table_price = serializers.IntegerField(required=False)
    deposit_percent = serializers.IntegerField(required=False)
    type_name = serializers.CharField()

    class Meta:
        model = LobType
        field = ['max_table_count', 'min_table_price', 'deposit_percent', 'type_name']


