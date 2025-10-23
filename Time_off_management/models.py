from django.db import models
from django.conf import settings
from django.db.models import JSONField
from tinymce.models import HTMLField
from django.utils import timezone
from Employee.models import *

# Create your models here.
LEAVE_STATUS = [
    ("DRAFT", "Draft"),
    ("PENDING", "Pending Approval"),
    ("APPROVED", "Approved"),
    ("REJECTED", "Rejected"),
    ("CANCELLED", "Cancelled"),
]

ATTENDANCE_STATUS = [
    ("PRESENT", "Present"),
    ("ABSENT", "Absent"),
    ("ON_LEAVE", "On Leave"),
    ("FIELD", "Field"),
]

EVENT_TYPE = [
    ("IN", "Check In"),
    ("OUT", "Check Out"),
    ("BREAK_START", "Break Start"),
    ("BREAK_END", "Break End"),
]



class Shift(models.Model):
    name = models.CharField(max_length=64)
    start_time = models.TimeField()
    end_time = models.TimeField()
    timezone = models.CharField(max_length=64, blank=True)
    is_flexible = models.BooleanField(default=False)
    breaks = JSONField(blank=True, default=list)  # list of {"start": "12:00", "end":"12:30"}
    notes =HTMLField(blank=True)

    def __str__(self):
        return self.name


class Holiday(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField()
    country = models.CharField(max_length=64, blank=True)
    is_recurring = models.BooleanField(default=False)
    description =HTMLField(blank=True)

    class Meta:
        unique_together = ("name", "date")

    def __str__(self):
        return f"{self.name} ({self.date})"


class LeaveType(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16, unique=True)
    description =HTMLField(blank=True)
    is_paid = models.BooleanField(default=True)
    max_per_year = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    requires_approval = models.BooleanField(default=True)
    carry_forward = models.BooleanField(default=False)
    accrual_rate_per_month = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class LeaveAllocation(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="allocations")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    allocated_days = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    used_days = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    carry_forwarded = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        unique_together = ("employee", "leave_type", "year")

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.year})"


class LeaveRequest(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    start_half_day = models.BooleanField(default=False)
    end_half_day = models.BooleanField(default=False)
    total_days = models.DecimalField(max_digits=6, decimal_places=2)
    reason =HTMLField(blank=True)
    attachment = models.FileField(upload_to="leave_attachments/", null=True, blank=True)
    status = models.CharField(max_length=16, choices=LEAVE_STATUS, default="DRAFT")
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="leave_created")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="leave_approved")
    approved_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta = JSONField(blank=True, default=dict)

    def submit(self, submitter=None):
        if self.status == "DRAFT":
            self.status = "PENDING"
            self.submitted_at = timezone.now()
            if submitter:
                self.created_by = submitter
            self.save()

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.start_date} to {self.end_date})"


class LeaveApproval(models.Model):
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE, related_name="approvals")
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    sequence = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=16, choices=LEAVE_STATUS, default="PENDING")
    comments =HTMLField(blank=True)
    acted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("sequence",)

    def __str__(self):
        return f"Approval {self.sequence} for {self.leave_request}"


class LeaveBalance(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="leave_balances")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    used = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("employee", "leave_type", "year")

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.year})"


class AttendanceEvent(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="events")
    timestamp = models.DateTimeField()
    event_type = models.CharField(max_length=16, choices=EVENT_TYPE)
    source = models.CharField(max_length=64, blank=True)
    device = models.CharField(max_length=128, blank=True)
    geo_location = models.CharField(max_length=128, blank=True)
    note =HTMLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-timestamp",)
    
    def __str__(self):
        return f"{self.employee} - {self.event_type} at {self.timestamp}"


class AttendanceRecord(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    shift = models.ForeignKey(Shift, null=True, blank=True, on_delete=models.SET_NULL)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    worked_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=16, choices=ATTENDANCE_STATUS, default="PRESENT")
    notes =HTMLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("employee", "date")
    
    def __str__(self):
        return f"Attendance {self.employee} - {self.date}"


class AttendanceCorrectionRequest(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="corrections")
    date = models.DateField()
    requested_check_in = models.TimeField(null=True, blank=True)
    requested_check_out = models.TimeField(null=True, blank=True)
    reason =HTMLField()
    attachment = models.FileField(upload_to="attendance_corrections/", null=True, blank=True)
    status = models.CharField(max_length=16, choices=LEAVE_STATUS, default="PENDING")
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Correction {self.employee} - {self.date}"


class OvertimeRequest(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="overtime_requests")
    date_from = models.DateField()
    date_to = models.DateField()
    total_hours = models.DecimalField(max_digits=5, decimal_places=2)
    reason =HTMLField(blank=True)
    status = models.CharField(max_length=16, choices=LEAVE_STATUS, default="PENDING")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class WorkWeek(models.Model):
    name = models.CharField(max_length=64, default="Default")
    configuration = JSONField(default=dict)  # e.g. {"mon": {"working": True, "start":"09:00","end":"17:00"}, ...}
    notes =HTMLField(blank=True)

    def __str__(self):
        return self.name