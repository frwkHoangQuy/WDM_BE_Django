from All_models.models import Service

from rest_framework import serializers


class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
