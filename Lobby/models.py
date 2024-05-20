# import uuid
#
# from django.db import models
#
# # Create your models here.
#
#
# class LobType(models.Model):
#     class Meta:
#         db_table = "LobType"
#     id = models.CharField(primary_key=True, default=uuid.uuid4().hex, editable=False, max_length=32)
#     max_table_count = models.IntegerField()
#     min_table_price = models.IntegerField()
#     deposit_percent = models.IntegerField()
#     created_at = models.DateTimeField(auto_now=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     type_name = models.CharField(max_length=191)
#     deleted_at = models.DateTimeField(null=True, default=None)
#
#
# class Lobby(models.Model):
#
#     class Meta:
#         db_table = "Lobby"
#
#     id = models.CharField(primary_key=True, default=uuid.uuid4().hex, max_length=32)
#     name = models.CharField(max_length=191)
#     lob_type = models.ForeignKey(LobType, on_delete=models.CASCADE)
