from Global_serializers.Lobby import LobbySerializers
from Global_serializers.Bill import BillSerializers
from Global_serializers.Customer import CustomerSerializers
from Global_serializers.Shift import ShiftSerializers

from All_models.models import Wedding, Customer, Shift, Lobby

from rest_framework import serializers


class CustomWeddingSerializers(serializers.ModelSerializer):
    Bill = BillSerializers(many=True, read_only=True)
    Customer = CustomerSerializers(source='customer', read_only=True)
    Lobby = LobbySerializers(source='lobby', read_only=True)
    shift = ShiftSerializers()

    class Meta:
        model = Wedding
        fields = ['id', 'groom', 'bride', 'wedding_date', 'shift', 'lobby', 'customer', 'table_count', 'created_at',
                  'updated_at', 'note', 'is_penalty_mode', 'Bill', 'Customer', 'Lobby']


class CustomCreateWeddingSerializers(serializers.ModelSerializer):
    phone = serializers.CharField()
    shift = serializers.CharField()
    lobby_id = serializers.CharField()

    class Meta:
        model = Wedding
        fields = ['groom', 'bride', 'table_count', 'note', 'wedding_date', 'shift', 'lobby_id', 'phone']

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        shift_name = validated_data.pop('shift')
        lobby_id = validated_data.pop('lobby_id')
        groom = validated_data.get('groom')
        bride = validated_data.get('bride')
        customer_name = f"{groom} & {bride}"
        try:
            lobby = Lobby.objects.get(id=lobby_id)
        except Lobby.DoesNotExist:
            raise serializers.ValidationError("Lobby with the given ID does not exist")
        customer, created = Customer.objects.get_or_create(phone=phone, defaults={'name': customer_name})
        shift, created = Shift.objects.get_or_create(name=shift_name)
        wedding = Wedding.objects.create(customer=customer, shift=shift, lobby=lobby, **validated_data)
        return wedding

