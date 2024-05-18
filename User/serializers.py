from rest_framework import serializers
from .models import User, Permission, Role, RolePermission
import uuid


class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'created_at', 'updated_at']

class UserSerializers(serializers.ModelSerializer):
    Role = RoleSerializers(source='role', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'display_name', 'username', 'password', 'role_id', 'created_at', 'updated_at', 'Role']


class PermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description', 'page', 'created_at', 'updated_at']


class RolePermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['role_id', 'permission_id', 'created_at', 'updated_at']


class CreateNewRoleSerializers(serializers.Serializer):
    name = serializers.CharField()



