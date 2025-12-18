from django.urls import path
from .views import *

# app_name = "Payroll"

urlpatterns = [
    path("payroll_processing/", payroll_processing, name="payroll_processing"),
    path("payroll_processing/create/", payroll_batch_create, name="payroll_batch_create"),
    path("payroll_processing/<int:pk>/", payroll_batch_detail, name="payroll_batch_detail"),
    
    path("salary_structure/", salary_structure, name="salary_structure"),
    path("salary_structure/create/", salary_structure_create, name="salary_structure_create"),
    path("salary_structure/<int:pk>/edit/", salary_structure_edit, name="salary_structure_edit"),
    path("salary_structure/<int:pk>/delete/", salary_structure_delete, name="salary_structure_delete"),
    
    path("deductions_benefits/", deductions_benefits, name="deductions_benefits"),
    path("deductions/create/", deduction_create, name="deduction_create"),
    path("deductions/<int:pk>/edit/", deduction_edit, name="deduction_edit"),
    path("deductions/<int:pk>/delete/", deduction_delete, name="deduction_delete"),
    
    path("benefits/create/", benefit_create, name="benefit_create"),
    path("benefits/<int:pk>/edit/", benefit_edit, name="benefit_edit"),
    path("benefits/<int:pk>/delete/", benefit_delete, name="benefit_delete"),
    
    path("loans_advances/", loans_advances, name="loans_advances"),
    path("loans_advances/create/", loan_create, name="loan_create"),
    path("loans_advances/<int:pk>/edit/", loan_edit, name="loan_edit"),
    path("loans_advances/<int:pk>/delete/", loan_delete, name="loan_delete"),
    path("loans_advances/<int:pk>/approve/", loan_approve, name="loan_approve"),
    path("loans_advances/<int:pk>/reject/", loan_reject, name="loan_reject"),
]
