from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from All_models.models import Food
from Global_serializers.Food import FoodSerializers


class FoodViews(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializers
