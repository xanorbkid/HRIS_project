from django.contrib import admin
from .models import JobOpening, Applicant, Interview, JobOffer, Onboarding


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "status", "employment_type", "posted_date", "closing_date")
    list_filter = ("status", "employment_type", "department")
    search_fields = ("title", "department__name", "job_title__name")
    ordering = ("-posted_date",)


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "job_opening", "status", "applied_at")
    list_filter = ("status", "job_opening__department")
    search_fields = ("first_name", "last_name", "email", "job_opening__title")


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ("applicant", "interview_type", "scheduled_date", "result")
    list_filter = ("interview_type", "result")
    search_fields = ("applicant__first_name", "applicant__last_name", "interviewer__username")


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ("applicant", "offered_position", "salary_offered", "status", "offer_date")
    list_filter = ("status",)
    search_fields = ("applicant__first_name", "applicant__last_name")


@admin.register(Onboarding)
class OnboardingAdmin(admin.ModelAdmin):
    list_display = ("employee", "task_name", "status", "due_date", "completed_at")
    list_filter = ("status",)
    search_fields = ("employee__user__username", "task_name")
