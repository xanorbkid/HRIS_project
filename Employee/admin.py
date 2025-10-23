from django.contrib import admin
from .models import *




@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'head')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level')
    search_fields = ('name', 'level')


class EmployeeDocumentInline(admin.TabularInline):
    model = EmployeeDocument
    extra = 1


class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 1


class JobAssignmentInline(admin.TabularInline):
    model = JobAssignment
    extra = 1


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'department', 'job_title', 'employment_type', 'status')
    list_filter = ('status', 'employment_type', 'department', 'job_title')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    inlines = [EmployeeDocumentInline, EmergencyContactInline, JobAssignmentInline]

    @admin.display(description='Employee Name')
    def get_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else '-'


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'review_date', 'score')
    list_filter = ('review_date', 'score')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'reviewer__email')


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'document_type', 'uploaded_at')
    search_fields = ('document_type', 'employee__user__email')
    list_filter = ('uploaded_at',)


@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('employee', 'name', 'relationship', 'phone')
    search_fields = ('name', 'phone', 'employee__user__email')


@admin.register(JobAssignment)
class JobAssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('title', 'employee__user__first_name', 'employee__user__last_name')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    search_fields = ('type_name',)
