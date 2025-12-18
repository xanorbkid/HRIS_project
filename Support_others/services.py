"""
Utility helpers for sending notifications throughout the platform.
"""

from __future__ import annotations

from typing import Optional, Sequence

import logging

from django.db import transaction
from django.contrib.auth import get_user_model

from .models import (
    Notification,
    NotificationCategory,
    NotificationLog,
    NotificationPreference,
)

logger = logging.getLogger(__name__)
User = get_user_model()


def _can_send_in_app(recipient: User, respect_preferences: bool) -> bool:
    """Return True if we should create an in-app notification."""
    if not respect_preferences:
        return True

    preference: Optional[NotificationPreference] = getattr(
        recipient, "notification_preferences", None
    )
    # If the employee never configured preferences, default to sending.
    if preference is None:
        return True

    return preference.in_app_enabled


@transaction.atomic
def send_notification(
    *,
    recipient: User,
    title: str,
    message: str,
    category: Optional[NotificationCategory] = None,
    channels: Optional[Sequence[str]] = None,
    respect_preferences: bool = True,
) -> Optional[Notification]:
    """
    Persist an in-app notification and log the delivery attempt.

    Parameters
    ----------
    recipient: User instance that should receive the notification.
    title/message: Content that will show up on the notification page and dropdown.
    category: Optional `NotificationCategory` for grouping/filtering.
    channels: Sequence of channels to log (defaults to ["IN_APP"]).
    respect_preferences: Skip creation when the user disabled in-app notifications.
    """
    if channels is None:
        channels = ["IN_APP"]

    if "IN_APP" in channels and not _can_send_in_app(recipient, respect_preferences):
        logger.info(
            "Skipping in-app notification for %s because preferences disabled it",
            recipient,
        )
        return None

    notification = Notification.objects.create(
        recipient=recipient,
        category=category,
        title=title.strip(),
        message=message,
    )

    for channel in channels:
        NotificationLog.objects.create(
            notification=notification,
            channel=channel,
            delivery_status="SENT",
        )

    return notification
