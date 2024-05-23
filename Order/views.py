from django.shortcuts import render, get_list_or_404
from All_models.models import Wedding, Customer

from Global_serializers.Customer import CustomerSerializers
from Global_serializers.Wedding import WeddingSerializers

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CustomWeddingSerializers, CustomCreateWeddingSerializers

from Authentication.Middleware.jwt_authentication import PermissionRequiredMixin


class OrderAccessPermission(PermissionRequiredMixin):
    permission_required = 'Process Orders'


class WeddingListView(OrderAccessPermission, APIView):
    def get(self, request):
        return Response([], status=200)


class WeddingCreateView(OrderAccessPermission, generics.CreateAPIView):
    queryset = Wedding.objects.all()
    serializer_class = CustomCreateWeddingSerializers


