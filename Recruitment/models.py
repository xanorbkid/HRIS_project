from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from Auth.models import SoftDeleteModel
from django.utils import timezone
from Employee.models import Department, JobTitle, EmployeeProfile

USER = settings.AUTH_USER_MODEL


# -----------------------------
# Job Openings
# -----------------------------
class JobOpening(SoftDeleteModel):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
        ("ON_HOLD", "On Hold"),
        ("FILLED", "Filled"),
    ]

    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True)
    employment_type = models.CharField(
        max_length=30,
        choices=[
            ("full_time", "Full Time"),
            ("part_time", "Part Time"),
            ("contract", "Contract"),
            ("internship", "Internship"),
        ],
        default="full_time"
    )
    location = models.CharField(max_length=200, blank=True)
    description = HTMLField(blank=True)
    requirements = HTMLField(blank=True)
    openings = models.PositiveIntegerField(default=1)
    salary_range = models.CharField(max_length=100, blank=True)
    posted_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name="job_posts")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    posted_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.department})"


# -----------------------------
# Applicants / Candidates
# -----------------------------
class Applicant(SoftDeleteModel):
    STATUS_CHOICES = [
        ("APPLIED", "Applied"),
        ("SCREENING", "Screening"),
        ("INTERVIEW", "Interview"),
        ("OFFERED", "Offered"),
        ("HIRED", "Hired"),
        ("REJECTED", "Rejected"),
    ]

    job_opening = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name="applicants")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    resume = models.FileField(upload_to="recruitment/resumes/", blank=True, null=True)
    cover_letter = HTMLField(blank=True)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    skills = models.TextField(blank=True)
    source = models.CharField(max_length=100, blank=True)  # e.g. LinkedIn, Referral, Website
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="APPLIED")
    applied_at = models.DateTimeField(auto_now_add=True)
    notes = HTMLField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_opening.title}"


# -----------------------------
# Interviews & Hiring
# -----------------------------
class Interview(SoftDeleteModel):
    INTERVIEW_TYPE = [
        ("PHONE", "Phone Interview"),
        ("TECHNICAL", "Technical Interview"),
        ("HR", "HR Interview"),
        ("FINAL", "Final Interview"),
    ]

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name="interviews")
    interviewer = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True)
    interview_type = models.CharField(max_length=50, choices=INTERVIEW_TYPE)
    scheduled_date = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    location = models.CharField(max_length=200, blank=True)
    feedback = HTMLField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    result = models.CharField(
        max_length=20,
        choices=[("PASSED", "Passed"), ("FAILED", "Failed"), ("PENDING", "Pending")],
        default="PENDING"
    )

    def __str__(self):
        return f"{self.applicant} - {self.interview_type}"


# -----------------------------
# Offer / Hiring
# -----------------------------
class JobOffer(SoftDeleteModel):
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE, related_name="offer")
    offered_position = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True)
    salary_offered = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    offer_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("ACCEPTED", "Accepted"),
            ("DECLINED", "Declined"),
            ("WITHDRAWN", "Withdrawn"),
        ],
        default="PENDING"
    )
    offer_letter = models.FileField(upload_to="recruitment/offers/", blank=True, null=True)
    remarks = HTMLField(blank=True)

    def __str__(self):
        return f"Offer for {self.applicant}"


# -----------------------------
# Onboarding
# -----------------------------
class Onboarding(SoftDeleteModel):
    TASK_STATUS = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="onboarding_tasks")
    task_name = models.CharField(max_length=200)
    description = HTMLField(blank=True)
    assigned_to = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks_assigned")
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default="PENDING")
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.task_name} - {self.employee}"
