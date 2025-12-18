from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.feedgenerator import Rss201rev2Feed
from django.urls import reverse

from .models import (
    Notification,
    Announcement,
    SupportTicket,
    TicketComment,
    NotificationPreference,
    AnnouncementSubscription,
)
from .services import send_notification
from .forms import AnnouncementForm
from Employee.models import EmployeeProfile


# -------------------------
# 🔔 Notifications
# -------------------------
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")
    preference, _ = NotificationPreference.objects.get_or_create(user=request.user)
    return render(
        request,
        "notifications.html",
        {
            "notifications": notifications,
            "preference": preference,
        },
    )


@login_required
@require_POST
def mark_all_notifications_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(
        is_read=True, read_at=timezone.now()
    )
    messages.success(request, "All notifications marked as read.")
    return redirect("support:notifications")


@login_required
def notification_settings_view(request):
    preference, _ = NotificationPreference.objects.get_or_create(user=request.user)
    if request.method == "POST":
        preference.email_enabled = bool(request.POST.get("email_enabled"))
        preference.sms_enabled = bool(request.POST.get("sms_enabled"))
        preference.in_app_enabled = bool(request.POST.get("in_app_enabled"))
        preference.save()
        messages.success(request, "Notification preferences updated.")
        return redirect("support:notification_settings")

    return render(request, "notification_settings.html", {"preference": preference})


# -------------------------
# 📰 Announcements / News
# -------------------------
@login_required
def announcements_view(request):
    announcements = Announcement.objects.filter(is_published=True).order_by("-created_at")
    subscription = AnnouncementSubscription.objects.filter(user=request.user).first()
    announcement_form = AnnouncementForm()
    return render(
        request,
        "announcements.html",
        {
            "announcements": announcements,
            "is_subscribed": bool(subscription),
            "announcement_form": announcement_form,
            "can_manage_announcements": request.user.is_staff,
        },
    )


@login_required
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, "announcement_detail.html", {"announcement": announcement})


def _ensure_can_manage(user):
    return user.is_staff


@login_required
def announcement_create(request):
    if request.method != "POST":
        return redirect("support:announcements")
    if not _ensure_can_manage(request.user):
        messages.error(request, "You do not have permission to create announcements.")
        return redirect("support:announcements")

    form = AnnouncementForm(request.POST)
    if form.is_valid():
        announcement = form.save(commit=False)
        announcement.author = request.user
        announcement.save()
        messages.success(request, "Announcement published.")
    else:
        messages.error(request, "Could not create announcement. Please fix the errors and try again.")
    return redirect("support:announcements")


@login_required
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method != "POST":
        return redirect("support:announcements")
    if not _ensure_can_manage(request.user):
        messages.error(request, "You do not have permission to edit announcements.")
        return redirect("support:announcements")

    form = AnnouncementForm(request.POST, instance=announcement)
    if form.is_valid():
        form.save()
        messages.success(request, "Announcement updated.")
    else:
        messages.error(request, "Unable to update announcement. Please fix the errors and try again.")
    return redirect("support:announcements")


@login_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        if not _ensure_can_manage(request.user):
            messages.error(request, "You do not have permission to delete announcements.")
        else:
            announcement.delete(user=request.user)
            messages.success(request, "Announcement deleted.")
    return redirect("support:announcements")


@login_required
@require_POST
def announcement_toggle_subscription(request):
    subscription = AnnouncementSubscription.all_objects.filter(user=request.user).first()
    if subscription and not subscription.is_deleted:
        subscription.delete()
        messages.info(request, "You have unsubscribed from announcements.")
    else:
        if subscription and subscription.is_deleted:
            subscription.restore()
        else:
            subscription = AnnouncementSubscription.objects.create(user=request.user)
        messages.success(request, "Subscribed to announcements digest.")
    return redirect("support:announcements")


@login_required
def announcements_rss_feed(request):
    feed = Rss201rev2Feed(
        title="Company Announcements",
        link=request.build_absolute_uri(request.path),
        description="Latest announcements from HRIS",
        language="en",
    )
    announcements = Announcement.objects.filter(is_published=True).order_by("-created_at")[:20]
    for ann in announcements:
        feed.add_item(
            title=ann.title,
            link=request.build_absolute_uri(reverse("support:announcement_detail", kwargs={"pk": ann.pk})),
            description=ann.content,
            pubdate=ann.created_at,
        )
    response = HttpResponse(content_type="application/rss+xml")
    feed.write(response, "utf-8")
    return response


# -------------------------
# 💬 Help & Support
# -------------------------
@login_required
def help_support_view(request):
    employee = EmployeeProfile.objects.filter(user=request.user).first()
    tickets = SupportTicket.objects.filter(employee=employee).order_by("-created_at")

    if request.method == "POST":
        subject = request.POST.get("subject")
        description = request.POST.get("description")
        if subject and description:
            ticket = SupportTicket.objects.create(
                employee=employee,
                subject=subject,
                description=description,
            )
            send_notification(
                recipient=request.user,
                title="Support ticket submitted",
                message=(
                    f"We've received your support ticket "
                    f"<strong>{ticket.subject}</strong>. You'll be notified here "
                    f"as it progresses."
                ),
            )
            messages.success(request, "Support ticket submitted successfully.")
            return redirect("support:help_support")

    return render(request, "help_support.html", {"tickets": tickets})
