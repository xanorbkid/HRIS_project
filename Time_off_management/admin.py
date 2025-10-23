from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time', 'is_flexible')
    search_fields = ('name',)
    list_filter = ('is_flexible',)


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'country', 'is_recurring')
    list_filter = ('country', 'is_recurring')
    search_fields = ('name',)


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_paid', 'max_per_year', 'requires_approval')
    list_filter = ('is_paid', 'requires_approval', 'carry_forward')
    search_fields = ('name', 'code')


@admin.register(LeaveAllocation)
class LeaveAllocationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'year', 'allocated_days', 'used_days', 'carry_forwarded')
    list_filter = ('year', 'leave_type')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'submitted_at')
    list_filter = ('status', 'leave_type', 'start_date', 'end_date')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'submitted_at')


@admin.register(LeaveApproval)
class LeaveApprovalAdmin(admin.ModelAdmin):
    list_display = ('leave_request', 'approver', 'sequence', 'status', 'acted_at')
    list_filter = ('status', 'sequence')
    search_fields = ('leave_request__employee__user__first_name', 'leave_request__employee__user__last_name')


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'year', 'balance', 'used')
    list_filter = ('year', 'leave_type')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')


@admin.register(AttendanceEvent)
class AttendanceEventAdmin(admin.ModelAdmin):
    list_display = ('employee', 'event_type', 'timestamp', 'source')
    list_filter = ('event_type', 'source')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    ordering = ('-timestamp',)


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'shift', 'check_in', 'check_out', 'status')
    list_filter = ('date', 'status', 'shift')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    ordering = ('-date',)


@admin.register(AttendanceCorrectionRequest)
class AttendanceCorrectionRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'processed_by', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    readonly_fields = ('created_at',)


@admin.register(OvertimeRequest)
class OvertimeRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date_from', 'date_to', 'total_hours', 'status')
    list_filter = ('status', 'date_from', 'date_to')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')


@admin.register(WorkWeek)
class WorkWeekAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
