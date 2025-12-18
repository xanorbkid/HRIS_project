from django.db import models
from django.conf import settings
from django.utils import timezone
from tinymce.models import HTMLField
from Auth.models import SoftDeleteModel
from Employee.models import EmployeeProfile

USER = settings.AUTH_USER_MODEL


class SalaryComponent(SoftDeleteModel):
    COMPONENT_TYPE = [
        ("EARNING", "Earning"),
        ("DEDUCTION", "Deduction"),
    ]
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=COMPONENT_TYPE)
    description = HTMLField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_taxable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class SalaryStructure(SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True)
    components = models.ManyToManyField(SalaryComponent, related_name="structures", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)

    def total_amount(self):
        return sum(c.amount for c in self.components.all())

    def __str__(self):
        return self.name


class TaxBracket(SoftDeleteModel):
    lower_limit = models.DecimalField(max_digits=12, decimal_places=2)
    upper_limit = models.DecimalField(max_digits=12, decimal_places=2)
    rate_percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.lower_limit} - {self.upper_limit} @ {self.rate_percent}%"


class PayrollBatch(SoftDeleteModel):
    batch_name = models.CharField(max_length=100)
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    generated_on = models.DateTimeField(default=timezone.now)
    processed_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("DRAFT", "Draft"), ("APPROVED", "Approved"), ("PAID", "Paid")],
        default="DRAFT"
    )

    def __str__(self):
        return f"{self.batch_name} ({self.status})"


class PayrollRecord(SoftDeleteModel):
    batch = models.ForeignKey(PayrollBatch, on_delete=models.CASCADE, related_name="records")
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=12, decimal_places=2)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.employee} - {self.net_salary}"


class PayrollAuditLog(SoftDeleteModel):
    payroll_record = models.ForeignKey(PayrollRecord, on_delete=models.CASCADE, related_name="audit_logs")
    action = models.CharField(max_length=100)
    performed_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action} by {self.performed_by}"


class Payslip(SoftDeleteModel):
    payroll_record = models.OneToOneField(PayrollRecord, on_delete=models.CASCADE, related_name="payslip")
    generated_at = models.DateTimeField(auto_now_add=True)
    remarks = HTMLField(blank=True)

    def __str__(self):
        return f"Payslip - {self.payroll_record.employee}"


class Deduction(SoftDeleteModel):
    name = models.CharField(max_length=100)
    description = HTMLField(blank=True)
    default_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Benefit(SoftDeleteModel):
    name = models.CharField(max_length=100)
    description = HTMLField(blank=True)
    taxable = models.BooleanField(default=True)
    default_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class EmployeeBenefit(SoftDeleteModel):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    effective_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.benefit.name} - {self.employee}"


class LoanAdvanceRequest(SoftDeleteModel):
    TYPE_CHOICES = [
        ("LOAN", "Loan"),
        ("ADVANCE", "Advance"),
    ]
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="loan_requests")
    request_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    reason = HTMLField(blank=True)
    request_date = models.DateField(default=timezone.now)
    approved_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="loans_approved")
    approval_status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("APPROVED", "Approved"), ("REJECTED", "Rejected")],
        default="PENDING"
    )
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    repayment_months = models.PositiveIntegerField(null=True, blank=True)
    start_repayment_date = models.DateField(null=True, blank=True)
    remarks = HTMLField(blank=True)

    def __str__(self):
        return f"{self.request_type} - {self.employee} ({self.amount_requested})"


class RepaymentSchedule(SoftDeleteModel):
    loan = models.ForeignKey(LoanAdvanceRequest, on_delete=models.CASCADE, related_name="repayments")
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    paid_on = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("PENDING", "Pending"), ("PAID", "Paid"), ("OVERDUE", "Overdue")],
        default="PENDING"
    )

    def __str__(self):
        return f"{self.loan.employee} - {self.due_date} ({self.status})"
