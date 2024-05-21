from All_models.models import User, Role, RolePermission, Permission
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta


def create_token_payload(username):
    data = {}
    permissionList = []
    user = User.objects.get(username=username)
    iat = datetime.utcnow()
    expiration_time = iat + timedelta(hours=1)
    exp = int(expiration_time.timestamp())

    try:
        role_id = str(user.role_id)
        role_permissions = RolePermission.objects.filter(role_id=role_id)
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
        roleData = Role.objects.get(id=user.role_id)
        role['id'] = role_id
        role['name'] = roleData.name
    except ObjectDoesNotExist:
        pass

    data['username'] = username
    data['sub'] = str(user.id)
    data['permissionList'] = permissionList
    data['role'] = role
    data['iat'] = iat.timestamp()
    data['exp'] = datetime.utcnow() + timedelta(hours=1)

    return data
