from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from All_models.models import User, Role
from .serializers import LoginSerializer, RegisterSerializer

import jwt

from .utils.create_token_payload import create_token_payload

from WDM_BE import settings


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
                payload = create_token_payload(username)
                
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({'access_token': token}, status=status.HTTP_200_OK)
            else:
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
                role_name = serializer.validated_data['role_name']

                existing_user = User.objects.filter(username=username).exists()
                if existing_user:
                    return Response({'error': 'Username đã tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    role = Role.objects.get(name=role_name)
                except Role.DoesNotExist:
                    return Response({'error': 'Role không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

                user = User(
                    username=username,
                    password=make_password(password),
                    display_name=display_name,
                    role_id=role.id
                )
                user.save()
                return Response({'message': 'Tạo người dùng thành công'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Thông tin không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyTokenViews(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return Response("Không có token được cung cấp", status=status.HTTP_401_UNAUTHORIZED)
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return Response("Token không hợp lệ", status=status.HTTP_401_UNAUTHORIZED)

        token = parts[1]
        try:
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return JsonResponse(decoded_payload)
        except jwt.ExpiredSignatureError:
            return Response("Token hết hạn", status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response("Token không hợp lệ", status=status.HTTP_401_UNAUTHORIZED)
