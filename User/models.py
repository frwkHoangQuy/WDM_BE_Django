from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=191)
    username = models.CharField(max_length=191, unique=True)
    password = models.CharField(max_length=191)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "User"
