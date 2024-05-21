from rest_framework import serializers
from All_models.models import User, Permission, Role, RolePermission
import uuid


class UserSerializers(serializers.Serializer):
    id = serializers.UUIDField()
    display_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    role_id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class PermissionSerializers(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    page = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class RoleSerializers(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class RolePermissionSerializers(serializers.Serializer):
    role_id = serializers.UUIDField()
    permission_id = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class CreateNewRoleSerializers(serializers.Serializer):
    name = serializers.CharField()
    permissionList = serializers.ListField()


class UpdatePermissionForRole(serializers.Serializer):
    roleID = serializers.CharField()
    permissionID = serializers.CharField()



