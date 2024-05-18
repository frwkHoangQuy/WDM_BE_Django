from django.db import models
import uuid


class Permission(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Role'


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    display_name = models.CharField(max_length=191)
    username = models.CharField(max_length=191, unique=True)
    password = models.CharField(max_length=191)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "User"


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'RolePermission'
        constraints = [
            models.UniqueConstraint(fields=['role', 'permission'], name='unique_role_permission')
        ]
        unique_together = [['role', 'permission']]