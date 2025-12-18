from django.contrib import admin
from .models import (
    SalaryComponent, SalaryStructure, TaxBracket,
    PayrollBatch, PayrollRecord, PayrollAuditLog, Payslip,
    Deduction, Benefit, EmployeeBenefit,
    LoanAdvanceRequest, RepaymentSchedule
)

@admin.register(SalaryComponent)
class SalaryComponentAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "amount", "is_taxable")
    search_fields = ("name",)
    list_filter = ("type", "is_taxable")

@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "created_by")
    filter_horizontal = ("components",)

@admin.register(TaxBracket)
class TaxBracketAdmin(admin.ModelAdmin):
    list_display = ("lower_limit", "upper_limit", "rate_percent")

@admin.register(PayrollBatch)
class PayrollBatchAdmin(admin.ModelAdmin):
    list_display = ("batch_name", "pay_period_start", "pay_period_end", "status", "processed_by")
    list_filter = ("status",)

@admin.register(PayrollRecord)
class PayrollRecordAdmin(admin.ModelAdmin):
    list_display = ("employee", "batch", "base_salary", "net_salary")
    search_fields = ("employee__first_name", "employee__last_name")

@admin.register(PayrollAuditLog)
class PayrollAuditLogAdmin(admin.ModelAdmin):
    list_display = ("payroll_record", "action", "performed_by", "timestamp")

@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ("payroll_record", "generated_at")

@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ("name", "default_amount")

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ("name", "taxable", "default_value")

@admin.register(EmployeeBenefit)
class EmployeeBenefitAdmin(admin.ModelAdmin):
    list_display = ("employee", "benefit", "value", "effective_date")

@admin.register(LoanAdvanceRequest)
class LoanAdvanceRequestAdmin(admin.ModelAdmin):
    list_display = ("employee", "request_type", "amount_requested", "approval_status", "request_date")
    list_filter = ("request_type", "approval_status")

@admin.register(RepaymentSchedule)
class RepaymentScheduleAdmin(admin.ModelAdmin):
    list_display = ("loan", "due_date", "amount_due", "status")
    list_filter = ("status",)
    search_fields = ("loan__employee__first_name", "loan__employee__last_name") 