from All_models.models import Bill

from rest_framework import serializers


class BillSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
