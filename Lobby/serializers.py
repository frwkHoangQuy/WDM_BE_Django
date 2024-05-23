from rest_framework import serializers
from Global_serializers.Wedding import WeddingSerializers
from All_models.models import Lobby, Wedding, Customer


class CustomLobbySerializers(serializers.ModelSerializer):
    Wedding = serializers.SerializerMethodField()

    class Meta:
        model = Lobby
        fields = ['id', 'name', 'lob_type_id', 'deleted_at', 'created_at', 'updated_at', 'Wedding']

    def get_Wedding(self, obj):
        filtered_weddings = self.context.get('filtered_weddings', None)
        if filtered_weddings is None:
            return WeddingSerializers(obj.weddings.all(), many=True).data
        return WeddingSerializers(filtered_weddings.filter(lobby=obj), many=True).data







