import csv

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import date, datetime, timedelta

from .forms import SignInForm
from Employee.models import Department, EmployeeProfile, Location, PerformanceReview
from Performances_developments.models import TrainingAttendance
from Recruitment.models import JobOpening
from Time_off_management.models import LeaveRequest

# ✅ SIGN UP (Register)
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            messages.success(request, "Account created successfully!")
            return redirect("dashboard")  # or wherever you want after login
    else:
        form = UserCreationForm()
    return render(request, "auth/signup.html", {"form": form})


# ✅ LOGIN (Sign In)
def login_view(request):
    if request.method == "POST":
        form = SignInForm(data=request.POST)
        if form.is_valid():
            # user = form.get_user()
            print("request==", request)
            print("username==", form.cleaned_data['username'])
            print("password==", form.cleaned_data['password'])
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')  # redirect to your main page
            else:
                messages.error(request, "Invalid username or password.")
            # # user = request.user
            # # login(request, user)
            # # messages.success(request, f"Welcome back, {user.username}!")
            # return redirect('/')  # redirect to your main page
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = SignInForm()
    if request.method == "POST":
        user = request.user
        logout(request)
        messages.success(request, f"You have been logged out successfully. Goodbye, {user.username}!")
        return redirect("login")
    # Show logout confirmation page
    return render(request, "auth/logout.html")

def _month_shift(base_date: date, offset: int) -> date:
    """Return the first day of the month, shifted by offset months (can be negative)."""
    year = base_date.year + ((base_date.month - 1 + offset) // 12)
    month = (base_date.month - 1 + offset) % 12 + 1
    return date(year, month, 1)


def _parse_month_param(raw_value: str | None) -> date | None:
    """Convert a YYYY-MM string from the month picker into a date object."""
    if not raw_value:
        return None
    try:
        parsed = datetime.strptime(raw_value, "%Y-%m")
    except (TypeError, ValueError):
        return None
    return parsed.date().replace(day=1)


def _build_dashboard_context(selected_month: date | None = None) -> dict:
    """Return dashboard metrics for the requested month (defaults to current month)."""
    today = timezone.localdate()
    reference_day = selected_month or today
    base_month = reference_day.replace(day=1)
    selected_month_str = selected_month.strftime("%Y-%m") if selected_month else None
    selected_month_query = f"?month={selected_month_str}" if selected_month_str else ""
    selected_month_display = base_month.strftime("%B %Y")

    total_employees = EmployeeProfile.objects.count()
    department_count = Department.objects.count()
    active_locations = Location.objects.count()

    on_leave_qs = LeaveRequest.objects.filter(
        status="APPROVED", start_date__lte=reference_day, end_date__gte=reference_day
    )
    on_leave_today = on_leave_qs.count()
    on_leave_percentage = (
        round((on_leave_today / total_employees) * 100, 1) if total_employees else 0
    )

    open_positions_qs = JobOpening.objects.filter(status="OPEN")
    open_positions = open_positions_qs.aggregate(
        total=Coalesce(Sum("openings"), 0)
    )["total"] or 0
    critical_roles = open_positions_qs.filter(openings__gte=3).count()

    current_window_start = reference_day - timedelta(days=30)
    previous_window_start = current_window_start - timedelta(days=30)
    hires_current = EmployeeProfile.objects.filter(
        date_joined__gte=current_window_start, date_joined__lt=reference_day
    ).count()
    hires_previous = EmployeeProfile.objects.filter(
        date_joined__gte=previous_window_start,
        date_joined__lt=current_window_start,
    ).count()
    if hires_previous:
        delta_percent = ((hires_current - hires_previous) / hires_previous) * 100
    else:
        delta_percent = hires_current * 100
    headcount_delta = f"{delta_percent:+.1f}%"

    staffing_trend = []
    for offset in range(5, -1, -1):
        period_start = _month_shift(base_month, -offset)
        period_end = _month_shift(base_month, -offset + 1)
        hires = EmployeeProfile.objects.filter(
            date_joined__gte=period_start, date_joined__lt=period_end
        ).count()
        exits = 0  # Attrition data not available
        staffing_trend.append(
            {
                "label": period_start.strftime("%b %Y"),
                "hires": hires,
                "exits": exits,
                "net": hires - exits,
            }
        )

    pending_leaves = (
        LeaveRequest.objects.select_related("employee", "leave_type")
        .filter(status="PENDING")
        .order_by("start_date")[:5]
    )

    if selected_month:
        recent_hires_start = selected_month
        recent_hires_end = _month_shift(selected_month, 1)
        recent_hires_period_label = selected_month_display
    else:
        recent_hires_end = reference_day + timedelta(days=1)
        recent_hires_start = reference_day - timedelta(days=30)
        recent_hires_period_label = "last 30 days"

    recent_hires = [
        {
            "name": emp.user.get_full_name() if emp.user else f"Employee {emp.id}",
            "department": emp.department.name if emp.department else "—",
            "start_date": emp.date_joined,
        }
        for emp in EmployeeProfile.objects.select_related("user", "department")
        .filter(date_joined__gte=recent_hires_start, date_joined__lt=recent_hires_end)
        .order_by("-date_joined")[:5]
    ]

    training_total = TrainingAttendance.objects.count()
    training_completed = TrainingAttendance.objects.filter(attended=True).count()
    training_completion = (
        f"{round((training_completed / training_total) * 100, 1)}%"
        if training_total
        else "0%"
    )

    performance_qs = PerformanceReview.objects.filter(
        review_date__gte=reference_day
    ).order_by("review_date")
    reviews_due = performance_qs.count()
    reviews_deadline = performance_qs.first().review_date if performance_qs.exists() else None

    return {
        "page_title": "HR Dashboard",
        "selected_month": selected_month_str,
        "selected_month_display": selected_month_display,
        "selected_month_query": selected_month_query,
        "reference_day": reference_day,
        "total_employees": total_employees,
        "headcount_delta": headcount_delta,
        "department_count": department_count,
        "active_locations": active_locations,
        "on_leave_today": on_leave_today,
        "on_leave_percentage": on_leave_percentage,
        "open_positions": open_positions,
        "critical_roles": critical_roles,
        "staffing_trend": staffing_trend,
        "pending_leaves": pending_leaves,
        "recent_hires": recent_hires,
        "recent_hires_period_label": recent_hires_period_label,
        "on_leave_requests": on_leave_qs,
        "training_completion": training_completion,
        "policy_acknowledged": "0%",
        "reviews_due": reviews_due,
        "reviews_deadline": reviews_deadline,
        "upcoming_birthdays": [],
        "risk_alerts": [],
    }


@login_required
def dashboard(request):
    selected_month = _parse_month_param(request.GET.get("month"))
    context = _build_dashboard_context(selected_month)
    context["dashboard_url"] = request.build_absolute_uri()
    return render(request, "dashboard.html", context)


@login_required
def dashboard_export(request):
    selected_month = _parse_month_param(request.GET.get("month"))
    context = _build_dashboard_context(selected_month)
    export_month = context["selected_month"] or timezone.localdate().strftime("%Y-%m")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="hr-dashboard-insights-{export_month}.csv"'
    )
    writer = csv.writer(response)

    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total headcount", context["total_employees"]])
    writer.writerow(["Headcount delta", context["headcount_delta"]])
    writer.writerow(["Departments", context["department_count"]])
    writer.writerow(["Active locations", context["active_locations"]])
    writer.writerow(["On leave today", context["on_leave_today"]])
    writer.writerow(["On leave %", f"{context['on_leave_percentage']}%"])
    writer.writerow(["Open positions", context["open_positions"]])
    writer.writerow(["Critical roles", context["critical_roles"]])
    writer.writerow(["Training completion", context["training_completion"]])
    writer.writerow(["Policy acknowledgements", context["policy_acknowledged"]])
    writer.writerow(["Reviews due", context["reviews_due"]])
    writer.writerow(
        ["Reviews deadline", context["reviews_deadline"] or "No pending reviews"]
    )

    writer.writerow([])
    writer.writerow(["Staffing Trend"])
    writer.writerow(["Month", "New hires", "Exits", "Net change"])
    for item in context["staffing_trend"]:
        writer.writerow([item["label"], item["hires"], item["exits"], item["net"]])

    writer.writerow([])
    writer.writerow(["Pending Leave Approvals"])
    writer.writerow(["Employee", "Leave type", "Dates"])
    for leave in context["pending_leaves"]:
        writer.writerow(
            [
                str(leave.employee),
                str(leave.leave_type),
                f"{leave.start_date} → {leave.end_date}",
            ]
        )

    if context["recent_hires"]:
        writer.writerow([])
        writer.writerow([f"Recent hires ({context['recent_hires_period_label']})"])
        writer.writerow(["Name", "Department", "Start date"])
        for hire in context["recent_hires"]:
            writer.writerow([hire["name"], hire["department"], hire["start_date"]])
    return response


@login_required
def workforce_report(request):
    selected_month = _parse_month_param(request.GET.get("month"))
    context = _build_dashboard_context(selected_month)
    context["page_title"] = "Workforce Movement Report"
    context["report_generated_at"] = timezone.now()
    return render(request, "reports/workforce_report.html", context)
>>>>>>> a3e4c76 (Initial project import)
