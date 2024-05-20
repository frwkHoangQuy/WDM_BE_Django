from django.db import models
import uuid


class Customer(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex, max_length=191)
    name = models.CharField(max_length=191)
    phone = models.CharField(max_length=191, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Customer'


class Shift(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex, max_length=191)
    name = models.CharField(max_length=191)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.CharField(default='null', max_length=191)

    class Meta:
        db_table = 'Shift'


class LobType(models.Model):
    class Meta:
        db_table = "LobType"
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex, editable=False, max_length=32)
    max_table_count = models.IntegerField()
    min_table_price = models.IntegerField()
    deposit_percent = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    type_name = models.CharField(max_length=191)
    deleted_at = models.CharField(default='null', max_length=191)


class Lobby(models.Model):

    class Meta:
        db_table = "Lobby"

    id = models.CharField(primary_key=True, default=uuid.uuid4().hex, max_length=32)
    name = models.CharField(max_length=191)
    lob_type = models.ForeignKey(LobType, on_delete=models.CASCADE)
    deleted_at = models.CharField(default='null', max_length=191)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class Wedding(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex, max_length=191)
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
    id = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=191)
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
    id = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=191)
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
    id = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=191)
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





