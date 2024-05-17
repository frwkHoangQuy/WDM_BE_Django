from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Permission, Role, RolePermission, User

from .serializers import CreateNewRoleSerializers


class UsersViews(APIView):

    def get(self, request):
        response_data = []
        users = User.objects.all()
        for user in users:
            try:
                role = Role.objects.get(id=user.role_id)
            except ObjectDoesNotExist:
                return Response({'error': 'Role không tồn tại'}, status=status.HTTP_400_BAD_REQUEST)
            temp = {
                'id': user.id,
                'display_name': user.display_name,
                'role_id': role.id,
                'username': user.username,
                'password': user.password,
                'created_at': user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            permissionList = []
            try:
                role_permissions = RolePermission.objects.filter(role_id=role.id)
                for role_permission in role_permissions:
                    permission = Permission.objects.get(id=role_permission.permission_id)
                    permissionList.append({
                        "id": str(permission.id),
                        "name": permission.name,
                        "description": permission.description,
                        "page": permission.page,
                        "created_at": permission.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": permission.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    })
            except ObjectDoesNotExist:
                pass
            temp['PermissionList'] = permissionList

            try:
                temp['role'] = role.name
            except ObjectDoesNotExist:
                temp['role'] = None

            response_data.append(temp)

        return Response(response_data)


class createRole(APIView):
    def post(self, request):
        serializer = CreateNewRoleSerializers(data=request.data)
        if serializer.is_valid():
            role = serializer.validated_data['name']
        try:
            exist = Role.objects.get(name=role)
        except ObjectDoesNotExist:
            Role(name=role).save()
        return Response("OK")


class DeleteUserByUsernameView(APIView):

    def delete(self, request, id):
        try:
            instance = User.objects.filter(id=id)
            instance.delete()
            return Response("Success")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_roles(request):
    permission = request.query_params.get('permission', 'false').lower() == 'true'

    try:
        if permission:
            roles = Role.objects.prefetch_related('rolepermission_set__permission').all()
            role_data = []
            for role in roles:
                role_permissions = role.rolepermission_set.all()
                permissions = [rp.permission for rp in role_permissions]
                role_data.append({
                    'id': role.id,
                    'name': role.name,
                    'created_at': role.created_at,
                    'updated_at': role.updated_at,
                    'permissions': [{'id': p.id, 'name': p.name, 'description': p.description, 'page': p.page} for p in permissions]
                })
        else:
            roles = Role.objects.all()
            role_data = [{'id': role.id, 'name': role.name, 'created_at': role.created_at, 'updated_at': role.updated_at} for role in roles]

        return Response(role_data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def update_role_permission(request):
    role_id = request.data.get('roleID')
    permission_id = request.data.get('permissionID')

    if not role_id or not permission_id:
        return Response({'error': 'roleID and permissionID are required'}, status=status.HTTP_400_BAD_REQUEST)
    role_id = role_id.replace('-', '')
    # permission_id = permission_id.replace('-', '')
    try:
        # Check if the role exists in the database
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({'error': 'Role does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the role already has the specified permission
        if RolePermission.objects.filter(role_id=role_id, permission_id=permission_id).exists():
            return Response({'error': f'Role ID: {role_id} already has permission: {permission_id}'}, status=status.HTTP_409_CONFLICT)
        
        # Create the role-permission association
        role_permission = RolePermission.objects.create(role_id=role_id, permission_id=permission_id)
        
        return Response({
            'role_id': role_permission.role_id,
            'permission_id': role_permission.permission_id,
            'created_at': role_permission.created_at,
            'updated_at': role_permission.updated_at
        }, status=status.HTTP_201_CREATED)

    except ObjectDoesNotExist as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def remove_role_permission(request):
    role_id = request.data.get('roleID')
    permission_id = request.data.get('permissionID')

    if not role_id or not permission_id:
        return Response({'error': 'role_id and permission_id are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if the role exists in the database
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({'error': 'Role does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the role has the specified permission
        role_permission_check = RolePermission.objects.filter(role_id=role_id, permission_id=permission_id)

        if not role_permission_check.exists():
            return Response({'error': f'Role ID: {role_id} does not have permission: {permission_id}'}, status=status.HTTP_409_CONFLICT)

        # Delete the role-permission association
        role_permission_check.delete()

        return Response({'message': 'Permission removed from role successfully'}, status=status.HTTP_204_NO_CONTENT)

    except ObjectDoesNotExist as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    