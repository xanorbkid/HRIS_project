import uuid
from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from Auth.models import SoftDeleteModel
from Employee.models import EmployeeProfile, Department

USER = settings.AUTH_USER_MODEL


# -----------------------------
# Employee HR Documents (separate from Employee app)
# -----------------------------
class HRDocument(SoftDeleteModel):
    """
    HR-managed documents related to an employee.
    Separate from EmployeeDocument in Employee app.
    """
    DOCUMENT_CATEGORY_CHOICES = [
        ("ID", "Identification"),
        ("CERT", "Certificate"),
        ("CONTRACT", "Contract"),
        ("APPRAISAL", "Appraisal"),
        ("OTHER", "Other"),
    ]

    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="hr_documents",
    )
    document_type = models.CharField(max_length=100, choices=DOCUMENT_CATEGORY_CHOICES, default="OTHER")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="hr_documents/")
    description = HTMLField(blank=True)
    uploaded_by = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_hr_docs",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    is_confidential = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.document_type}) - {self.employee}"


# -----------------------------
# Company Policies & Forms
# -----------------------------
class CompanyPolicy(SoftDeleteModel):
    CATEGORY_CHOICES = [
        ("HR", "Human Resources"),
        ("IT", "Information Technology"),
        ("FIN", "Finance"),
        ("GEN", "General"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="GEN")
    file = models.FileField(upload_to="company_policies/")
    description = HTMLField(blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="policies",
    )
    effective_date = models.DateField()
    uploaded_by = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="policies_uploaded",
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.category})"


# -----------------------------
# Contracts & Letters
# -----------------------------
class ContractOrLetter(SoftDeleteModel):
    CONTRACT_TYPE_CHOICES = [
        ("EMPLOYMENT", "Employment Contract"),
        ("PROMOTION", "Promotion Letter"),
        ("TERMINATION", "Termination Letter"),
        ("NOTICE", "Notice Letter"),
        ("OTHER", "Other"),
    ]

    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="contracts_letters",
    )
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPE_CHOICES, default="OTHER")
    title = models.CharField(max_length=200)
    issued_date = models.DateField(auto_now_add=True)
    issued_by = models.ForeignKey(
        USER,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issued_contracts",
    )
    file = models.FileField(upload_to="contracts_letters/")
    notes = HTMLField(blank=True)
    valid_until = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.contract_type}) - {self.employee}"
