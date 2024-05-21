from All_models.models import Food

from rest_framework import serializers


class FoodSerializers(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'price', 'status', 'created_at',
                  'updated_at', 'deleted_at', 'inventory']
