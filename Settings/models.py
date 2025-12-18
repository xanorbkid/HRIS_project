import uuid

from django.conf import settings
from django.contrib.auth.models import Permission
from django.db import models


class Function(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Function"
        verbose_name_plural = "Functions"

    def __str__(self):
        return self.name


class TypeOfService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Type of Service"
        verbose_name_plural = "Types of Service"

    def __str__(self):
        return self.name


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_of_service = models.ForeignKey(
        TypeOfService, on_delete=models.CASCADE, related_name="services"
    )
    name = models.CharField(max_length=255, unique=True)
    level = models.PositiveIntegerField(default=1)
    parent_service = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="child_services",
    )

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ["type_of_service__name", "level", "name"]

    def __str__(self):
        return self.name


class Responsibility(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Responsibility"
        verbose_name_plural = "Responsibilities"

    def __str__(self):
        return self.name


class PermissionGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="settings_permission_groups",
        help_text="Permissions bundled under this group.",
    )

    class Meta:
        verbose_name = "Permission Group"
        verbose_name_plural = "Permission Groups"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    permission_groups = models.ManyToManyField(
        PermissionGroup, blank=True, related_name="roles"
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="settings_roles",
        help_text="Fine-grained permissions assigned directly to the role.",
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="RoleAssignment",
        blank=True,
        related_name="custom_roles",
    )

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["name"]

    def __str__(self):
        return self.name


class RoleAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, related_name="assignments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="role_assignments"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Role Assignment"
        verbose_name_plural = "Role Assignments"
        unique_together = ("role", "user")
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.user} → {self.role}"
