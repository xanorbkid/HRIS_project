from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')


@admin.action(description="Soft Delete Selected")
def soft_delete(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete(user=request.user)
        ActivityLog.objects.create(user=request.user, action='delete',
            object_type=obj.__class__.__name__, object_id=obj.id)

@admin.action(description="Restore Selected")
def restore_objects(modeladmin, request, queryset):
    for obj in queryset:
        obj.restore()
        ActivityLog.objects.create(user=request.user, action='restore',
            object_type=obj.__class__.__name__, object_id=obj.id)
