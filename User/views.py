from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Permission, Role, RolePermission, User
from .serializers import UserSerializers, RoleSerializers, PermissionSerializers, RolePermissionSerializers


class UsersViews(APIView):

    def get(self, request):
        response_data = []
        users = User.objects.all()
        role_permissions = RolePermission.objects.all()
        permissions = Permission.objects.all()
        roles = Role.objects.all()

        users_serializers = UserSerializers(users, many=True).data
        role_permissions_serializers = RolePermissionSerializers(role_permissions, many=True).data
        permissions_serializers = PermissionSerializers(permissions, many=True).data
        roles_serializers = RoleSerializers(roles, many=True).data

        role_dict = {role['id']: role['name'] for role in roles_serializers}

        user_permissions_roles = {}
        for role_permission in role_permissions_serializers:
            role_id = role_permission['role_id']
            permission_id = role_permission['permission_id']

            for user in users_serializers:
                user_role_id = user['role_id']
                if user_role_id == role_id:
                    if user['id'] not in user_permissions_roles:
                        user_permissions_roles[user['id']] = {
                            "id": user['id'],
                            "display_name": user['display_name'],
                            "username": user['username'],
                            "password": user['password'],
                            "created_at": user['created_at'],
                            "updated_at": user['updated_at'],
                            "role_id": user['role_id'],
                            "PermissionList": [],
                            "role": role_dict.get(role_id, "")
                        }
                    for permission in permissions_serializers:
                        if permission['id'] == permission_id:
                            user_permissions_roles[user['id']]["PermissionList"].append(permission)

        response_data = list(user_permissions_roles.values())



        return Response(response_data)
