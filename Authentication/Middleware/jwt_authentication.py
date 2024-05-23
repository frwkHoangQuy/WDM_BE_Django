from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from All_models.models import User
from django.views import View
from django.http import JsonResponse

from WDM_BE import settings

import logging


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                parts = auth_header.split()
                if len(parts) != 2 or parts[0].lower() != 'bearer':
                    return Response("Token không hợp lệ", status=status.HTTP_401_UNAUTHORIZED)

                token = parts[1]
                print(token)
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(username=payload['username'])
                request.user = user
                permissions = []
                for permission in payload['permissionList']:
                    permissions.append(permission['name'])
                request.user_permissions = permissions
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                request.user = None
                request.user_permissions = []
        else:
            request.user = None
            request.user_permissions = []


class PermissionRequiredMixin:
    permission_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.permission_required and self.permission_required not in request.user_permissions:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        raise PermissionDenied("Bạn không có quyền truy cập.")


