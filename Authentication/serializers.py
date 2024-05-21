from rest_framework import serializers
from All_models.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    display_name = serializers.CharField()
    role_name = serializers.CharField()
