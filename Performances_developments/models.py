import uuid
from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from django.utils import timezone
from Auth.models import SoftDeleteModel
from Employee.models import EmployeeProfile  # ✅ Linking to existing employee model

USER = settings.AUTH_USER_MODEL


class ReviewCycle(SoftDeleteModel):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# class PerformanceReview(SoftDeleteModel):
    # REVIEW_STATUS = [
    #     ("PENDING", "Pending"),
    #     ("IN_PROGRESS", "In Progress"),
    #     ("COMPLETED", "Completed"),
    # ]

    # employee = models.ForeignKey(
    #     EmployeeProfile, 
    #     on_delete=models.CASCADE, 
    #     related_name="deleted_performance_dev_items"
    # )
    # reviewer = models.ForeignKey(
    #     USER, 
    #     on_delete=models.SET_NULL, 
    #     null=True, 
    #     blank=True, 
    #     related_name="given_reviews"
    # )
    # cycle = models.ForeignKey(
    #     ReviewCycle, 
    #     on_delete=models.SET_NULL, 
    #     null=True, 
    #     blank=True
    # )
    # review_date = models.DateField(default=timezone.now)
    # overall_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # strengths = HTMLField(blank=True)
    # weaknesses = HTMLField(blank=True)
    # recommendations = HTMLField(blank=True)
    # status = models.CharField(max_length=20, choices=REVIEW_STATUS, default="PENDING")

    # def __str__(self):
    #     return f"{self.employee} - {self.cycle}"


class Goal(SoftDeleteModel):
    STATUS = [
        ("NOT_STARTED", "Not Started"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("DEFERRED", "Deferred"),
    ]

    employee = models.ForeignKey(
        EmployeeProfile, 
        on_delete=models.CASCADE, 
        related_name="performance_goals"
    )
    title = models.CharField(max_length=200)
    description = HTMLField(blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS, default="NOT_STARTED")

    def __str__(self):
        return f"{self.title} ({self.employee})"


class TrainingProgram(SoftDeleteModel):
    title = models.CharField(max_length=200)
    description = HTMLField(blank=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    trainer = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title


class TrainingAttendance(SoftDeleteModel):
    training = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name="attendance_records")
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    feedback = HTMLField(blank=True)

    def __str__(self):
        return f"{self.employee} - {self.training}"


class Promotion(SoftDeleteModel):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="promotions")
    previous_position = models.CharField(max_length=200)
    new_position = models.CharField(max_length=200)
    effective_date = models.DateField(default=timezone.now)
    remarks = HTMLField(blank=True)

    def __str__(self):
        return f"Promotion: {self.employee} → {self.new_position}"


class Warning(SoftDeleteModel):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="warnings")
    issued_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    warning_date = models.DateField(default=timezone.now)
    reason = HTMLField()
    action_taken = HTMLField(blank=True)
    severity = models.CharField(
        max_length=20,
        choices=[("MINOR", "Minor"), ("MAJOR", "Major"), ("CRITICAL", "Critical")],
        default="MINOR"
    )

    def __str__(self):
        return f"Warning for {self.employee} - {self.severity}"
