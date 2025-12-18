from django.db import models
from django.conf import settings
from Auth.models import SoftDeleteModel
from Employee.models import EmployeeProfile, PerformanceReview
from Payroll.models import Payslip
from Time_off_management.models import LeaveRequest, ATTENDANCE_STATUS

USER = settings.AUTH_USER_MODEL


class SelfServiceActivityLog(SoftDeleteModel):
    """Tracks what the employee viewed or updated in self-service."""
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="self_service_logs")
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee} - {self.action} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
