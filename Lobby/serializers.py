from rest_framework import serializers
from .models import LobType


class LobTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LobType
        fields = ["id", "max_table_count", "min_table_price", "deposit_percent",
                  "created_at", "updated_at", "type_name","deleted_at"]