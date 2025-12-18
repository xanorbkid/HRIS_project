from django.contrib import admin
from .models import SelfServiceActivityLog

@admin.register(SelfServiceActivityLog)
class SelfServiceActivityLogAdmin(admin.ModelAdmin):
    list_display = ("employee", "action", "timestamp")
    search_fields = ("employee__user__username", "action")
    list_filter = ("timestamp",)
