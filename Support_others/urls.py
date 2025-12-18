from django.urls import path
from .views import (
    notifications_view,
    mark_all_notifications_read,
    notification_settings_view,
    announcements_view,
    announcement_detail,
    announcement_create,
    announcement_edit,
    announcement_delete,
    announcement_toggle_subscription,
    announcements_rss_feed,
    help_support_view,
)

app_name = "support"

urlpatterns = [
    # 🔔 Notifications
    path("notifications/", notifications_view, name="notifications"),
    path("notifications/mark-all-read/", mark_all_notifications_read, name="notifications_mark_read"),
    path("notifications/settings/", notification_settings_view, name="notification_settings"),

    # 📰 Announcements / News
    path("announcements/", announcements_view, name="announcements"),
    path("announcements/<int:pk>/", announcement_detail, name="announcement_detail"),
    path("announcements/create/", announcement_create, name="announcement_create"),
    path("announcements/<int:pk>/edit/", announcement_edit, name="announcement_edit"),
    path("announcements/<int:pk>/delete/", announcement_delete, name="announcement_delete"),
    path("announcements/subscribe/", announcement_toggle_subscription, name="announcements_subscribe"),
    path("announcements/rss/", announcements_rss_feed, name="announcements_rss"),

    # 💬 Help & Support
    path("help-support/", help_support_view, name="help_support"),
]
