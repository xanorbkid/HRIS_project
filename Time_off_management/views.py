from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import *
from .forms import LeaveRequestForm, HolidayForm, AttendanceRecordForm

# Create your views here.
@login_required
def attendance_list(request):
    records = AttendanceRecord.objects.select_related('employee', 'shift').all().order_by("-date")
    current_employee = getattr(request.user, "employee_profile", None)
    context = {
        'page_title': 'Attendance Records',
        'records': records,
        'attendance_form': AttendanceRecordForm(),
        'can_manage_attendance': request.user.is_staff,
        'default_attendance_employee': current_employee.id if current_employee else '',
        'default_attendance_date': timezone.localdate().isoformat(),
    }
    return render(request, 'attendance_list.html', context)


@login_required
def attendance_create(request):
    if request.method != "POST":
        return redirect("attendance_list")
    if not request.user.is_staff:
        messages.error(request, "You are not allowed to add attendance records.")
        return redirect("attendance_list")

    form = AttendanceRecordForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Attendance recorded.")
    else:
        messages.error(request, "Unable to create attendance record. Please fix the errors.")
    return redirect("attendance_list")


@login_required
def attendance_edit(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    if request.method != "POST":
        return redirect("attendance_list")
    if not request.user.is_staff:
        messages.error(request, "You are not allowed to edit attendance records.")
        return redirect("attendance_list")

    form = AttendanceRecordForm(request.POST, instance=record)
    if form.is_valid():
        form.save()
        messages.success(request, "Attendance updated.")
    else:
        messages.error(request, "Unable to update attendance. Please fix the errors.")
    return redirect("attendance_list")


@login_required
def attendance_delete(request, pk):
    record = get_object_or_404(AttendanceRecord, pk=pk)
    if request.method == "POST":
        if not request.user.is_staff:
            messages.error(request, "You are not allowed to delete attendance records.")
        else:
            record.delete(user=request.user)
            messages.success(request, "Attendance record removed.")
    return redirect("attendance_list")

@login_required
def shift_list(request):
    shifts = Shift.objects.all()
    context = {
        'page_title': 'Shift Management',
        'shifts': shifts,
    }
    return render(request, 'shift.html', context)

@login_required
def leave_request_list(request):
    leaves = LeaveRequest.objects.select_related('employee', 'leave_type').all()
    context = {
        'page_title': 'Leave & Time-Off Requests',
        'leaves': leaves,
    }
    return render(request, 'leave_request.html', context)

@login_required
def holiday_list(request):
    holidays = Holiday.objects.all().order_by("date")
    context = {
        'page_title': 'Work Calendar / Holidays',
        'holidays': holidays,
        'holiday_form': HolidayForm(),
    }
    return render(request, 'holiday.html', context)


@login_required
def holiday_create(request):
    if request.method != "POST":
        return redirect("holiday_list")

    form = HolidayForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Holiday added successfully.")
    else:
        messages.error(request, "Unable to add holiday. Please correct the errors and try again.")
    return redirect("holiday_list")


@login_required
def holiday_edit(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method != "POST":
        return redirect("holiday_list")

    form = HolidayForm(request.POST, instance=holiday)
    if form.is_valid():
        form.save()
        messages.success(request, "Holiday updated successfully.")
    else:
        messages.error(request, "Unable to update holiday. Please correct the errors and try again.")
    return redirect("holiday_list")


@login_required
def holiday_delete(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == "POST":
        holiday.delete(user=request.user)
        messages.success(request, "Holiday deleted.")
    return redirect("holiday_list")


def leave_create(request):
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user  # if logged in user submits
            leave.save()
            return redirect("leave-list")
    else:
        form = LeaveRequestForm()

    return render(request, "leave_form.html", {"form": form, "page_title": "New Leave Request"})
