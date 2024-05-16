from django.db import models
import uuid


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=191)
    description = models.CharField(max_length=191, null=True, blank=True)
    page = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Permission'
        constraints = [
            models.UniqueConstraint(fields=['page'], name='Permission_page_key')
        ]


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=191, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Role'


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=191)
    username = models.CharField(max_length=191, unique=True)
    password = models.CharField(max_length=191)
    role_id = models.UUIDField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "User"


class RolePermission(models.Model):
    role_id = models.UUIDField()
    permission_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'RolePermission'
        constraints = [
            models.UniqueConstraint(fields=['role_id', 'permission_id'], name='unique_role_permission')
        ]
