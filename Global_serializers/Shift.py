from All_models.models import Shift

from rest_framework import serializers


class ShiftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'
