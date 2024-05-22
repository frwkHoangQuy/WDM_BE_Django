from django.shortcuts import render, get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from Global_serializers.Food import FoodSerializers

from All_models.models import Food, Service


class UploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, model):
        id = request.data.get('id')
        image = request.data.get('image')

        if not id or not image:
            return Response({"error": "Missing required data"}, status=400)

        instance = get_object_or_404(model, id=id)

        if instance.image == image:
            instance.save()
        else:
            instance.image = image
            instance.save()

        return Response("Update Success", status=200)


class UploadFoodImage(UploadView):

    def post(self, request):
        return super().post(request, Food)


class UploadServiceImage(UploadView):

    def post(self, request):
        return super().post(request, Service)



