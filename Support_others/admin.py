from django.contrib import admin
from .models import (
    NotificationCategory, Notification, NotificationLog,
    AnnouncementCategory, Announcement, AnnouncementAttachment, AnnouncementView,
    SupportCategory, SupportTicket, TicketAttachment, TicketComment, SupportFAQ
)

# -------- NOTIFICATIONS --------
@admin.register(NotificationCategory)
class NotificationCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_deleted")
    search_fields = ("name",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "recipient", "category", "is_read", "created_at")
    list_filter = ("category", "is_read", "created_at")
    search_fields = ("title", "message", "recipient__username")


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("notification", "channel", "delivery_status", "sent_at")
    list_filter = ("channel", "delivery_status")


# -------- ANNOUNCEMENTS --------
@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


class AnnouncementAttachmentInline(admin.TabularInline):
    model = AnnouncementAttachment
    extra = 1


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "is_published", "start_date", "end_date")
    list_filter = ("category", "is_published")
    search_fields = ("title", "content")
    inlines = [AnnouncementAttachmentInline]


@admin.register(AnnouncementView)
class AnnouncementViewAdmin(admin.ModelAdmin):
    list_display = ("announcement", "employee", "viewed_at")
    list_filter = ("viewed_at",)


# -------- HELP & SUPPORT --------
@admin.register(SupportCategory)
class SupportCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 1


class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 1


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "employee", "category", "status", "priority", "assigned_to", "created_at")
    list_filter = ("status", "priority", "category")
    search_fields = ("subject", "description")
    inlines = [TicketAttachmentInline, TicketCommentInline]


@admin.register(SupportFAQ)
class SupportFAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("question", "answer")
