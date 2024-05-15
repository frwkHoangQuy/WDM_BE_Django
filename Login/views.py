from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import LoginSerializer, RegisterSerializer

import jwt

from datetime import datetime, timedelta


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            if check_password(password, user.password):
                expiration_time = datetime.utcnow() + timedelta(hours=1)
                payload = {'user_id': str(user.id), 'exp': expiration_time}
                token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
                return Response({'token': token}, status=status.HTTP_200_OK)
            else:
                print("Authentication failed: Invalid credentials")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        try:
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                display_name = serializer.validated_data['display_name']
                user = User(username=username, password=make_password(password), display_name=display_name)
                user.save()
                return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteUserByUsernameView(APIView):

    def delete(self, request, username):
        try:
            instance = User.objects.filter(username=username)
            instance.delete()
            return HttpResponse("Success")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
