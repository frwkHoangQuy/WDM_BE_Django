from django.contrib.auth.hashers import check_password, make_password
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
import time
from django.views.decorators.csrf import csrf_exempt

from User.models import User, Role
from .serializers import LoginSerializer, RegisterSerializer
from .utils.create_token_payload import create_token_payload


class LoginView(APIView):

    def post(self, request):
        print(123)
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
                print("Authentication failed: Invalid credentials")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        try:
            if serializer.is_valid():

                # Kiểm tra dữ liệu trả về
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                display_name = serializer.validated_data['display_name']
                role_name = serializer.validated_data['role_name']
                
                # Kiểm tra sự tồn tại của người dùng
                existing_user = User.objects.filter(username=username).exists()
                if existing_user:
                    return Response({'error': 'Username đã tồn tại'}, status=status.HTTP_400_BAD_REQUEST)
                # Kiểm tra sự tồn tại của Role
                try:
                    role = Role.objects.get(name=role_name)
                except Role.DoesNotExist:
                    return Response({'error': 'Role không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)

                user = User(username=username, password=make_password(password),
                    display_name=display_name, role_id=role.id)
                user.save()
                return Response({'Tạo người dùng thành công'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'Lỗi: Thông tin không hợp lệ'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def verify_token(request):
    token = request.headers.get('Authorization', '').split('Bearer ')
    if len(token) != 2:
        return JsonResponse({'error': 'Token is missing'}, status=401)
    token = token[1]
    print(token)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return JsonResponse({'data': payload}, status=200)
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)
