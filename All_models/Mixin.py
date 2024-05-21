from django.db import models
from django.utils import timezone


class SoftDelete(models.Model):
    deleted_at = models.CharField(default=None, null=True, max_length=191)

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    def except_soft_delete(self, **kwargs):
        return super().filter(deleted_at__isnull=True, **kwargs)

    def soft_deleted(self):
        return super().filter(deleted_at__isnull=False)
