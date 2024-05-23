from All_models.models import Wedding
from rest_framework import serializers


class WeddingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = '__all__'
