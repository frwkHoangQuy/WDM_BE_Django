from All_models.models import Food

from rest_framework import serializers


class FoodSerializers(serializers.ModelSerializer):
    class Meta:
        db_table = 'Food'
        fields = '__all__'
