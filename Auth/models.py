from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
    

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username



class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='deleted_%(class)s_items'
    )

    # Managers: default manager filters out soft-deleted objects
    class SoftDeleteQuerySet(models.QuerySet):
        def delete(self, user=None):
            # bulk soft-delete: set flags and timestamp
            return self.update(is_deleted=True, deleted_at=timezone.now())

        def hard_delete(self):
            return super().delete()

    class SoftDeleteManager(models.Manager):
        def get_queryset(self):
            return SoftDeleteModel.SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, user=None, using=None, keep_parents=False):
        """Soft delete and track the user who did it."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        if user:
            self.deleted_by = user
        self.save()

    def restore(self, user=None):
        """Restore a soft-deleted instance."""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        """Actual database delete"""
        super().delete(using=using, keep_parents=keep_parents)


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('restore', 'Restore'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    object_type = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField(null=True, blank=True)  # Store field changes

    def __str__(self):
        return f"{self.user} {self.action} {self.object_type} ({self.object_id})"
 