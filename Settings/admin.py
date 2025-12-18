from django.contrib import admin

from .models import (
    Function,
    PermissionGroup,
    Responsibility,
    Role,
    RoleAssignment,
    Service,
    TypeOfService,
)


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    search_fields = ("name",)


@admin.register(TypeOfService)
class TypeOfServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "type_of_service", "level", "parent_service")
    list_filter = ("type_of_service", "level")
    search_fields = ("name",)


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    search_fields = ("name",)


class RoleAssignmentInline(admin.TabularInline):
    model = RoleAssignment
    extra = 0
    autocomplete_fields = ("user",)


@admin.register(PermissionGroup)
class PermissionGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "permission_count")
    search_fields = ("name",)
    filter_horizontal = ("permissions",)

    @staticmethod
    def permission_count(obj):
        return obj.permissions.count()


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "assigned_users")
    list_filter = ("is_active",)
    search_fields = ("name",)
    filter_horizontal = ("permission_groups", "permissions")
    inlines = [RoleAssignmentInline]

    @staticmethod
    def assigned_users(obj):
        return obj.users.count()


@admin.register(RoleAssignment)
class RoleAssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "assigned_at")
    search_fields = (
        "user__username",
        "user__email",
        "role__name",
    )
    autocomplete_fields = ("user", "role")
