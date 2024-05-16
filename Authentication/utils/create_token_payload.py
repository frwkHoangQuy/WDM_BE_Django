from User.models import User, Role, RolePermission, Permission
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta


def create_token_payload(username):
    data = {}
    permissionList = []
    user = User.objects.get(username=username)
    expiration_time = datetime.utcnow() + timedelta(hours=1)
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
    role = {}
    try:
        roles = Role.objects.get(id=user.role_id)
        role['id'] = str(roles.id)
        role['name'] = roles.name
    except ObjectDoesNotExist:
        pass

    data['username'] = username
    data['sub'] = str(user.id)
    data['permissionList'] = permissionList
    data['role'] = role
    data['exp'] = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    return data
