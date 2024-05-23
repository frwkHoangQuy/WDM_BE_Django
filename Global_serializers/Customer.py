from All_models.models import Customer

from rest_framework import serializers


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
