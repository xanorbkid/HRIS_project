from __future__ import annotations

from typing import Dict, Any

from .models import Notification


def navbar_notifications(request) -> Dict[str, Any]:
    """
    Inject the latest notifications + unread count into every template.
    """
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {
            "navbar_notifications": [],
            "navbar_unread_notifications": 0,
        }

    user_notifications = Notification.objects.filter(recipient=user)
    recent_notifications = user_notifications.order_by("-created_at")[:5]
    unread_count = user_notifications.filter(is_read=False).count()

    return {
        "navbar_notifications": recent_notifications,
        "navbar_unread_notifications": unread_count,
    }
