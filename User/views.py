from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import logging

from All_models.models import Permission, Role, RolePermission, User

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
                        'permissions': [{'id': p.id, 'name': p.name, 'description': p.description, 'page': p.page}
                                        for p in permissions]
                    })
            else:
                roles = Role.objects.all()
                role_data = [
                    {'id': role.id, 'name': role.name, 'created_at': role.created_at, 'updated_at': role.updated_at}
                    for role in roles
                ]

            return Response(role_data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.error("Role not found", exc_info=True)
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError:
            logger.error("Database error", exc_info=True)
            return Response({'error': 'A database error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error("An unexpected error occurred", exc_info=True)
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
                return Response({"error": "Role already exists"}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                try:
                    Role(name=role).save()
                    return Response("Create Success", status=status.HTTP_201_CREATED)
                except IntegrityError as e:
                    logger.error(f"Integrity error while creating role: {str(e)}")
                    return Response({"error": "Integrity error occurred"}, status=status.HTTP_400_BAD_REQUEST)
                except DatabaseError as e:
                    logger.error(f"Database error while creating role: {str(e)}")
                    return Response({"error": "Database error occurred"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    logger.error(f"Unexpected error while creating role: {str(e)}", exc_info=True)
                    return Response({"error": "An unexpected error occurred"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_permission_for_role(self, request):
        serializer = UpdatePermissionForRole(data=request.data)
        if serializer.is_valid():
            roleID = serializer.validated_data['roleID']
            permissionID = serializer.validated_data['permissionID']
            try:
                RolePermission.objects.create(permission_id=permissionID, role_id=roleID)
                return Response("Update Success", status=status.HTTP_200_OK)
            except IntegrityError as e:
                logger.error(f"Integrity error while updating permission: {str(e)}")
                return Response({"error": "Integrity error occurred"}, status=status.HTTP_400_BAD_REQUEST)
            except DatabaseError as e:
                logger.error(f"Database error while updating permission: {str(e)}")
                return Response({"error": "Database error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                logger.error(f"Unexpected error while updating permission: {str(e)}", exc_info=True)
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleDeleteViews(APIView):
    def delete(self, request, id):
        try:
            delete_role = Role.objects.get(id=id)
            delete_role.delete()
            return Response("Xóa thành công", status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            logger.error(f"Role with id {id} does not exist")
            return Response({"error": "Không tìm thấy Role"}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError as e:
            logger.error(f"Database error while deleting role: {str(e)}")
            return Response({"error": "Database error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Unexpected error while deleting role: {str(e)}", exc_info=True)
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemovePermissionForRole(APIView):
    def delete(self, request):
        try:
            roleID = request.data['roleID']
            permissionID = request.data['permissionID']
            role_permission = RolePermission.objects.get(permission_id=permissionID, role_id=roleID)
            role_permission.delete()
            return Response("OK", status=status.HTTP_200_OK)
        except RolePermission.DoesNotExist:
            logger.error(f"RolePermission with roleID {roleID} and permissionID {permissionID} does not exist")
            return Response({"error": "Không tìm thấy RolePermission"}, status=status.HTTP_404_NOT_FOUND)
        except DatabaseError as e:
            logger.error(f"Database error while removing permission: {str(e)}")
            return Response({"error": "Database error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError as e:
            logger.error(f"Key error: {str(e)}")
            return Response({"error": f"Missing key: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error while removing permission: {str(e)}", exc_info=True)
            return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class UpdateRoleForUser(APIView):
    def post(self, request):
        user_id = request.data.get('userID')
        role_id = request.data.get('roleID')

        if not user_id or not role_id:
            logger.error("userID and roleID are required.")
            return Response({"error": "userID and roleID are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.error(f"User with id {user_id} not found.")
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            logger.error(f"Role with id {role_id} not found.")
            return Response({"error": "Role not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            update_user.role = role
            update_user.save()
        except DatabaseError as e:
            logger.error(f"Database error while updating the role for user {user_id}: {str(e)}", exc_info=True)
            return Response({"error": "Database error occurred while updating the role."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Unexpected error while updating the role for user {user_id}: {str(e)}", exc_info=True)
            return Response({"error": f"An error occurred while updating the role: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info(f"Role for user {user_id} updated successfully to role {role_id}.")
        return Response({"message": "Role updated successfully."}, status=status.HTTP_200_OK)


class UpdateNameForUser(APIView):
    def patch(self, request, id):
        try:
            display_name = request.data['display_name']
        except KeyError:
            logger.error("Display name is required.")
            return Response({"error": "Display name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            update_user = User.objects.get(id=id)
        except User.DoesNotExist:
            logger.error(f"User with id {id} not found.")
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            update_user.display_name = display_name
            update_user.save()
        except ValidationError as e:
            logger.error(f"Validation error for user {id}: {str(e)}", exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            logger.error(f"Database error while updating the display name for user {id}: {str(e)}", exc_info=True)
            return Response({"error": "Database error occurred while updating the display name."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Unexpected error while updating the display name for user {id}: {str(e)}", exc_info=True)
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info(f"Display name for user {id} updated successfully.")
        return Response({"message": "Display name updated successfully."}, status=status.HTTP_200_OK)
