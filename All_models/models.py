import uuid
from django.db import models
from .Mixin import SoftDelete, SoftDeleteManager


class Customer(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    name = models.CharField(max_length=191)
    phone = models.CharField(max_length=191, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Customer'


class Shift(SoftDelete):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    name = models.CharField(max_length=191)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.CharField(default=None, null=True, max_length=191)

    objects = SoftDeleteManager()

    class Meta:
        db_table = 'Shift'


class LobType(SoftDelete):
    class Meta:
        db_table = "LobType"
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    max_table_count = models.IntegerField()
    min_table_price = models.IntegerField()
    deposit_percent = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    type_name = models.CharField(max_length=191)
    deleted_at = models.CharField(default=None, null=True, max_length=191)

    objects = SoftDeleteManager()


class Lobby(SoftDelete):
    class Meta:
        db_table = "Lobby"
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    name = models.CharField(max_length=191)
    lob_type = models.ForeignKey(LobType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SoftDeleteManager()


class Wedding(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    groom = models.CharField(max_length=191)
    bride = models.CharField(max_length=191)
    wedding_date = models.DateTimeField()
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    lobby = models.ForeignKey(Lobby, on_delete=models.CASCADE, related_name='weddings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customers')
    table_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=191, null=True, blank=True)
    is_penalty_mode = models.BooleanField(default=True)

    class Meta:
        db_table = 'Wedding'


class ServiceOrder(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    service_id = models.CharField(max_length=191)
    service_name = models.CharField(max_length=191)
    service_price = models.IntegerField()
    note = models.CharField(max_length=191, null=True, blank=True)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ServiceOrder'


class FoodOrder(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    food_id = models.CharField(max_length=191)
    food_name = models.CharField(max_length=191)
    food_price = models.IntegerField()
    count = models.IntegerField()
    note = models.CharField(max_length=191, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE)

    class Meta:
        db_table = 'FoodOrder'


class Bill(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    service_total_price = models.IntegerField()
    food_total_price = models.IntegerField()
    total_price = models.IntegerField()
    deposit_require = models.IntegerField()
    deposit_amount = models.IntegerField()
    remain_amount = models.IntegerField()
    extra_fee = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Bill'


class Permission(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
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
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    name = models.CharField(max_length=191, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Role'


class User(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=36)
    display_name = models.CharField(max_length=191)
    username = models.CharField(max_length=191, unique=True)
    password = models.CharField(max_length=191)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
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


class Food(SoftDelete):
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=191)
    name = models.CharField(max_length=191, null=False)
    price = models.IntegerField(null=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inventory = models.IntegerField(null=False)

    class Meta:
        db_table = "Food"
