import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from tinymce.models import HTMLField
from Auth.models import SoftDeleteModel
from Employee.models import EmployeeProfile, Department

USER = settings.AUTH_USER_MODEL


# -------------------------------- 
# NOTIFICATIONS & ALERTS
# --------------------------------
class NotificationCategory(SoftDeleteModel):
    """Categories for grouping notifications."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name 


class Notification(SoftDeleteModel):
    """Individual notification messages for users."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    recipient = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="notifications")
    category = models.ForeignKey(NotificationCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    message = HTMLField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def mark_as_read(self):
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.title} → {self.recipient}"


class NotificationLog(SoftDeleteModel):
    """Tracks system notifications sent to users (email, SMS, in-app)."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="logs")
    channel = models.CharField(
        max_length=20,
        choices=[
            ("IN_APP", "In App"),
            ("EMAIL", "Email"),
            ("SMS", "SMS"),
        ],
        default="IN_APP"
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(
        max_length=20,
        choices=[
            ("SENT", "Sent"),
            ("FAILED", "Failed"),
            ("PENDING", "Pending"),
        ],
        default="PENDING"
    )
    error_message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.channel} log for {self.notification}"


# --------------------------------
# ANNOUNCEMENTS & NEWS
# --------------------------------
class AnnouncementCategory(SoftDeleteModel):
    """Categories for announcements, e.g., HR Updates, Events, General."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Announcement(SoftDeleteModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    content = HTMLField()
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AnnouncementAttachment(SoftDeleteModel):
    """Attachments such as policy PDFs or images."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="announcements/attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.announcement}"


class AnnouncementView(SoftDeleteModel):
    """Tracks which employees viewed each announcement."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="views")
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} viewed {self.announcement}"


# --------------------------------
# HELP & SUPPORT
# --------------------------------
class SupportCategory(SoftDeleteModel):
    """Categories for support requests (IT, HR, Payroll, Facilities, etc.)."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SupportTicket(SoftDeleteModel):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
        ("CLOSED", "Closed"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("URGENT", "Urgent"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="support_tickets")
    category = models.ForeignKey(SupportCategory, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=255)
    description = HTMLField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="MEDIUM")
    assigned_to = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets_assigned"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} ({self.status})"


class TicketAttachment(SoftDeleteModel):
    """Employees or admins can attach files to a ticket."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="support/attachments/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Attachment for {self.ticket}"


class TicketComment(SoftDeleteModel):
    """Threaded comments between employee and support staff."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(USER, on_delete=models.CASCADE)
    comment = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    internal_only = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author} on {self.ticket}"


class SupportFAQ(SoftDeleteModel):
    """Frequently asked questions related to help topics."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    category = models.ForeignKey(SupportCategory, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.CharField(max_length=255)
    answer = HTMLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class NotificationPreference(SoftDeleteModel):
    """Per-user notification delivery preferences."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(USER, on_delete=models.CASCADE, related_name="notification_preferences")
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    in_app_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification preferences for {self.user}"


class AnnouncementSubscription(SoftDeleteModel):
    """Tracks if a user is subscribed to announcements digest."""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(USER, on_delete=models.CASCADE, related_name="announcement_subscription")
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} announcement subscription"
