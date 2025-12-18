from django.contrib import admin
from .models import HRDocument, CompanyPolicy, ContractOrLetter


@admin.register(HRDocument)
class HRDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "employee", "document_type", "uploaded_by", "uploaded_at", "is_confidential")
    list_filter = ("document_type", "is_confidential", "uploaded_at")
    search_fields = ("title", "employee__first_name", "employee__last_name")
    readonly_fields = ("uploaded_at",)


@admin.register(CompanyPolicy)
class CompanyPolicyAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "department", "effective_date", "is_active")
    list_filter = ("category", "is_active", "department")
    search_fields = ("title", "description")
    readonly_fields = ("effective_date",)


@admin.register(ContractOrLetter)
class ContractOrLetterAdmin(admin.ModelAdmin):
    list_display = ("title", "employee", "contract_type", "issued_date", "issued_by", "valid_until")
    list_filter = ("contract_type", "issued_date")
    search_fields = ("title", "employee__first_name", "employee__last_name")
    readonly_fields = ("issued_date",)
