from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Debug thông tin đăng nhập
            print(f"Attempting login with username: {username} and password: {password}")

            # Sử dụng phương thức authenticate để xác thực người dùng
            user = authenticate(request, username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
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
