from django.shortcuts import render, get_object_or_404

from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from All_models.models import Food
from Global_serializers.Food import FoodSerializers


class FoodViews(generics.ListAPIView):
    queryset = Food.objects.except_soft_delete()
    serializer_class = FoodSerializers


class FoodCreateViews(generics.CreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializers


class FoodEditViews(generics.UpdateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializers
    lookup_field = 'id'


class FoodSoftDeleteViews(APIView):
    def patch(self, request, id):
        soft_delete_food = get_object_or_404(Food, id=id)
        soft_delete_food.soft_delete()
        return Response({"detail": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)

