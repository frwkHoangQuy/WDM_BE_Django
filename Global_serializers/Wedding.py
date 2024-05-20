from All_models.models import Wedding
from rest_framework import serializers


class WeddingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = ['id', 'groom', 'bride', 'wedding_date', 'shift',
                  'customer', 'table_count', 'note', 'is_penalty_mode']
