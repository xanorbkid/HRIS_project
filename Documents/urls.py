from django.urls import path
from .views import *

# app_name = "Documents"

urlpatterns = [
    path("employee-documents/", employee_documents, name="employee_documents"),
    path("company-policies/", company_policies, name="company_policies"),
    path("contracts-letters/", contracts_letters, name="contracts_letters"),
    path('upload/', upload_document, name='upload_document'),
    path('generate_contract/', generate_contract, name='generate_contract'),
    path('upload/', upload_policy, name='upload_policy'),
]
