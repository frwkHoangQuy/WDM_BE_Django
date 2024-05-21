from rest_framework import serializers
from Global_serializers.Wedding import WeddingSerializers
from All_models.models import Lobby


class CustomLobbySerializers(serializers.ModelSerializer):
    weddings = serializers.SerializerMethodField()

    class Meta:
        model = Lobby
        fields = ['id', 'name', 'lob_type_id', 'deleted_at', 'weddings']

    def get_weddings(self, obj):
        filtered_weddings = self.context.get('filtered_weddings', None)
        if filtered_weddings is None:
            return []
        return WeddingSerializers(weddings, many=True).data
