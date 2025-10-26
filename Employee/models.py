from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from Auth.models import SoftDeleteModel
# from time_off_management.models import *

USER = settings.AUTH_USER_MODEL

class Department(SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True)
    description = HTMLField(blank=True)
    head = models.ForeignKey('EmployeeProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    def __str__(self):
        return self.name


class JobTitle(SoftDeleteModel):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True)
    description = HTMLField(blank=True)

    def __str__(self):
        return self.name


class EmployeeProfile(SoftDeleteModel):
    user = models.OneToOneField(
        USER, on_delete=models.CASCADE, null=True, blank=True,
        related_name='employee_profile'
    )
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    job_title = models.ForeignKey(JobTitle, null=True, blank=True, on_delete=models.SET_NULL)
    manager = models.ForeignKey('self', null=True, blank=True,
                                on_delete=models.SET_NULL, related_name='team_members')

    date_joined = models.DateField()
    employment_type = models.CharField(max_length=20, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('intern', 'Intern'),
    ])
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bank_details = models.JSONField(blank=True, null=True)
    # work_schedule = models.ForeignKey("Shift", null=True, blank=True, on_delete=models.SET_NULL)

    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('terminated', 'Terminated'),
        ('on_leave', 'On Leave'),
    ], default='active')

    def __str__(self):
        return self.user.get_full_name() if self.user else f"Employee {self.id}"

class EmployeeDocument(SoftDeleteModel):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='employee_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} for {self.employee}"
    
class EmergencyContact(SoftDeleteModel):
    RELATIONSHIP_CHOICES = [
        ('mother', 'Mother'),
        ('father', 'Father'),
        ('brother', 'Brother'),
        ('sister', 'Sister'),
        ('spouse', 'Spouse'),
        ('friend', 'Friend'),
        ('other', 'Other'),
    ]
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relationship}) for {self.employee}"
    

# A temporary, task-based, or project-specific responsibility assigned to the employee (Project Lead, Acting Manager, etc.)
class JobAssignment(SoftDeleteModel):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = HTMLField(blank=True)

    def __str__(self):
        return f"{self.title} assignment for {self.employee}"
    
class PerformanceReview(SoftDeleteModel):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name='performance_reviews')
    reviewer = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, related_name='reviews_given')
    review_date = models.DateField()
    score = models.IntegerField()
    comments = HTMLField(blank=True)

    def __str__(self):
        return f"Performance Review for {self.employee} on {self.review_date}"
    
class Location(SoftDeleteModel):
    name = models.CharField(max_length=100)
    address = HTMLField(blank=True)

    def __str__(self):
        return self.name
    
class EmploymentType(SoftDeleteModel):
    type_name = models.CharField(max_length=50)
    description = HTMLField(blank=True)

    def __str__(self):
        return self.type_name
