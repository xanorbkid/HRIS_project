from django.contrib import admin
from .models import (
    ReviewCycle,
    Goal,
    TrainingProgram,
    TrainingAttendance,
    Promotion,
    Warning,
)

@admin.register(ReviewCycle)
class ReviewCycleAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("-start_date",)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "employee", "start_date", "end_date", "status", "progress")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("title", "employee__user__username", "employee__user__first_name")
    ordering = ("-start_date",)


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "trainer", "start_date", "end_date", "location")
    list_filter = ("start_date", "end_date")
    search_fields = ("title", "trainer__username")
    ordering = ("-start_date",)


@admin.register(TrainingAttendance)
class TrainingAttendanceAdmin(admin.ModelAdmin):
    list_display = ("training", "employee", "attended")
    list_filter = ("attended",)
    search_fields = ("training__title", "employee__user__username")
    ordering = ("training",)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("employee", "previous_position", "new_position", "effective_date")
    list_filter = ("effective_date",)
    search_fields = ("employee__user__username", "previous_position", "new_position")
    ordering = ("-effective_date",)


@admin.register(Warning)
class WarningAdmin(admin.ModelAdmin):
    list_display = ("employee", "issued_by", "warning_date", "severity")
    list_filter = ("severity", "warning_date")
    search_fields = ("employee__user__username", "issued_by__username", "reason")
    ordering = ("-warning_date",)
