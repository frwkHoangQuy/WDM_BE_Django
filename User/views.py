from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .models import Permission, Role, RolePermission, User

from .serializers import CreateNewRoleSerializers, UpdatePermissionForRole


class UsersViews(APIView):

    def get(self, request):
        pass

    def delete(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass


class PermissionViews(UsersViews):

    def get(self, request):
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
                        'permissions': [{'id': p.id, 'name': p.name, 'description': p.description, 'page': p.page} for p
                                        in permissions]
                    })
            else:
                roles = Role.objects.all()
                role_data = [
                    {'id': role.id, 'name': role.name, 'created_at': role.created_at, 'updated_at': role.updated_at} for
                    role in roles]

            return Response(role_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        pass

    def post(self, request):
        action = request.query_params.get('action')
        if action == 'create_role':
            return self.create_role(request)
        elif action == 'update_permission_for_role':
            return self.update_permission_for_role(request)
        return Response({"message": "Action not specified or unknown"}, status=status.HTTP_400_BAD_REQUEST)

    def create_role(self, request):
        serializer = CreateNewRoleSerializers(data=request.data)
        if serializer.is_valid():
            role = serializer.validated_data['name']
            try:
                exist = Role.objects.get(name=role)
            except ObjectDoesNotExist:
                Role(name=role).save()
                return Response("Create Success", status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_permission_for_role(self, request):
        serializer = UpdatePermissionForRole(data=request.data)
        print(request.data)
        if serializer.is_valid():
            roleID = serializer.validated_data['roleID']
            permissionID = serializer.validated_data['permissionID']
            RolePermission(permission_id=permissionID, role_id=roleID).save()
            return Response(status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleDeleteViews(PermissionViews):
    def delete(self, request, id):
        try:
            delete_role = Role.objects.get(id=id)
            delete_role.delete()
            return Response("Xóa thành công")
        except Role.DoesNotExist:
            return Response("Không tìm thấy Role")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RemovePermissionForRole(PermissionViews):

    def delete(self, request):
        roleID = request.data['roleID']
        permissionID = request.data['permissionID']
        RolePermission.objects.get(permission_id=permissionID, role_id=roleID).delete()
        return Response("OK")


class AccountInformationView(UsersViews):

    def get(self, request):
        response_data = []
        users = User.objects.all()
        for user in users:
            try:
                role = Role.objects.get(id=user.role_id)
            except Role.DoesNotExist:
                role = Role.objects.get(name='Admin')
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
                        "id": permission.id,
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

    def delete(self, request, id):
        try:
            instance = User.objects.filter(id=id)
            instance.delete()
            return Response("Success")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        pass


class UpdateRoleForUser(UsersViews):
    def post(self, request):
        user_id = request.data.get('userID')
        role_id = request.data.get('roleID')

        if not user_id or not role_id:
            return Response({"error": "userID and roleID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({"error": "Role not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            update_user.role = role
            update_user.save()
        except Exception as e:
            return Response({"error": f"An error occurred while updating the role: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Role updated successfully."}, status=status.HTTP_200_OK)


class UpdateNameForUser(UsersViews):
    def patch(self, request, id):
        display_name = request.data['display_name']
        try:
            update_user = User.objects.get(id=id)
            update_user.display_name = display_name
            update_user.save()
        except ObjectDoesNotExist:
            return Response(status=500)
        return Response("OK")
