from All_models.models import Service

from rest_framework import serializers


class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'price', 'status', 'created_at',
                  'updated_at', 'deleted_at', 'inventory']
