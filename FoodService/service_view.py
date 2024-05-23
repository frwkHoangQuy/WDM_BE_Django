from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from All_models.models import Service
from Global_serializers.Service import ServiceSerializers

from Authentication.Middleware.jwt_authentication import PermissionRequiredMixin


class ServiceViewsAccessPermission(PermissionRequiredMixin):
    permission_required = 'Manage Food Service'


class ServiceViews(ServiceViewsAccessPermission, generics.ListAPIView):
    queryset = Service.objects.except_soft_delete()
    serializer_class = ServiceSerializers


class ServiceCreateViews(ServiceViewsAccessPermission, generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers


class ServiceEditViews(ServiceViewsAccessPermission, generics.UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers
    lookup_field = 'id'


class ServiceSoftDeleteViews(ServiceViewsAccessPermission, APIView):
    def patch(self, request, id):
        print(id)
        soft_delete_service = get_object_or_404(Service, id=id)
        soft_delete_service.soft_delete()
        return Response({"detail": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
