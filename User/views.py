from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Permission, Role, RolePermission, User

from .serializers import CreateNewRoleSerializers


class UsersViews(APIView):

    def get(self, request):
        response_data = []
        users = User.objects.all()
        for user in users:
            try:
                role = user.role_id
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
                role_permissions = RolePermission.objects.filter(role_id=user.role_id)
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
                role = user.role_id
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


class getRole(APIView):

    def get(self, request):
        permission_param = request.query_params.get('permission')
        print(permission_param)
        if permission_param and permission_param.lower() == 'true':
            roles = self.get_roles_based_on_permissions()
            return Response(roles)
        else:
            return Response({"error": "Invalid permission parameter"}, status=400)

    def get_roles_based_on_permissions(self):
        data_response = []
        roles = Role.objects.all()
        for role in roles:
            temp = {}
            temp['id'] = role.id
            temp['name'] = role.name
            temp['created_at'] = role.created_at
            temp['updated_at'] = role.updated_at
            data_response.append(temp)
            permission_list = []
            roles_permissions = RolePermission.objects.filter(role_id=role.id)
            for role_permission in roles_permissions:
                role_permission_temp = {}
                role_permission_temp['role_id'] = role_permission.role_id
                role_permission_temp['permission_id'] = role_permission.permission_id
                role_permission_temp['created_at'] = role_permission.created_at
                role_permission_temp['updated_at'] = role_permission.updated_at
                permission = Permission.objects.get(id=role_permission.permission_id)
                role_permission_temp['name'] = permission.name
                role_permission_temp['description'] = permission.description
                role_permission_temp['page'] = permission.page
                permission_list.append(role_permission_temp)
            temp['permissions'] = permission_list
        return data_response

