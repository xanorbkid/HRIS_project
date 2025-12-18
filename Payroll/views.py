from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    PayrollBatch, SalaryStructure, Deduction, Benefit,
    LoanAdvanceRequest
)
from .forms import DeductionForm, BenefitForm, LoanAdvanceRequestForm, PayrollBatchForm, SalaryStructureForm


@login_required
def payroll_processing(request):
    batches = PayrollBatch.objects.all().order_by("-generated_on")
    return render(request, "payroll_processing.html", {"batches": batches})


@login_required
def payroll_batch_create(request):
    form = PayrollBatchForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        batch = form.save(commit=False)
        batch.processed_by = request.user
        batch.save()
        messages.success(request, "Payroll batch created successfully.")
        return redirect("payroll_processing")
    return render(request, "payroll_batch_form.html", {"form": form, "page_title": "Create Payroll Batch"})


@login_required
def payroll_batch_detail(request, pk):
    batch = get_object_or_404(PayrollBatch, pk=pk)
    return render(request, "payroll_batch_detail.html", {"batch": batch})


@login_required
def salary_structure(request):
    structures = SalaryStructure.objects.prefetch_related("components").all()
    return render(request, "salary_structure.html", {"structures": structures})


@login_required
def salary_structure_create(request):
    form = SalaryStructureForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        structure = form.save(commit=False)
        structure.created_by = request.user
        structure.save()
        form.save_m2m()
        messages.success(request, "Salary structure created successfully.")
        return redirect("salary_structure")
    return render(request, "salary_structure_form.html", {"form": form, "page_title": "Create Salary Structure"})


@login_required
def salary_structure_edit(request, pk):
    structure = get_object_or_404(SalaryStructure, pk=pk)
    form = SalaryStructureForm(request.POST or None, instance=structure)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Salary structure updated successfully.")
        return redirect("salary_structure")
    return render(request, "salary_structure_form.html", {"form": form, "page_title": f"Edit Salary Structure - {structure.name}"})


@login_required
def salary_structure_delete(request, pk):
    structure = get_object_or_404(SalaryStructure, pk=pk)
    if request.method == "POST":
        structure.delete()
        messages.success(request, "Salary structure deleted successfully.")
        return redirect("salary_structure")
    return render(request, "salary_structure_delete.html", {"structure": structure})


@login_required
def deductions_benefits(request):
    deductions = Deduction.objects.all()
    benefits = Benefit.objects.all()
    return render(request, "deductions_benefits.html", {"deductions": deductions, "benefits": benefits})


@login_required
def deduction_create(request):
    form = DeductionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Deduction created successfully.")
        return redirect("deductions_benefits")
    return render(request, "deduction_form.html", {"form": form, "page_title": "Add Deduction"})


@login_required
def deduction_edit(request, pk):
    deduction = get_object_or_404(Deduction, pk=pk)
    form = DeductionForm(request.POST or None, instance=deduction)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Deduction updated successfully.")
        return redirect("deductions_benefits")
    return render(request, "deduction_form.html", {"form": form, "page_title": f"Edit Deduction - {deduction.name}"})


@login_required
def deduction_delete(request, pk):
    deduction = get_object_or_404(Deduction, pk=pk)
    if request.method == "POST":
        deduction.delete()
        messages.success(request, "Deduction deleted successfully.")
        return redirect("deductions_benefits")
    return render(request, "deduction_delete.html", {"deduction": deduction})


@login_required
def benefit_create(request):
    form = BenefitForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Benefit created successfully.")
        return redirect("deductions_benefits")
    return render(request, "benefit_form.html", {"form": form, "page_title": "Add Benefit"})


@login_required
def benefit_edit(request, pk):
    benefit = get_object_or_404(Benefit, pk=pk)
    form = BenefitForm(request.POST or None, instance=benefit)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Benefit updated successfully.")
        return redirect("deductions_benefits")
    return render(request, "benefit_form.html", {"form": form, "page_title": f"Edit Benefit - {benefit.name}"})


@login_required
def benefit_delete(request, pk):
    benefit = get_object_or_404(Benefit, pk=pk)
    if request.method == "POST":
        benefit.delete()
        messages.success(request, "Benefit deleted successfully.")
        return redirect("deductions_benefits")
    return render(request, "benefit_delete.html", {"benefit": benefit})


@login_required
def loans_advances(request):
    loans = LoanAdvanceRequest.objects.select_related("employee").all()
    return render(request, "loans_advances.html", {"loans": loans})


@login_required
def loan_create(request):
    form = LoanAdvanceRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Loan/Advance request created successfully.")
        return redirect("loans_advances")
    return render(request, "loan_form.html", {"form": form, "page_title": "Create Loan/Advance Request"})


@login_required
def loan_edit(request, pk):
    loan = get_object_or_404(LoanAdvanceRequest, pk=pk)
    form = LoanAdvanceRequestForm(request.POST or None, instance=loan)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Loan/Advance request updated successfully.")
        return redirect("loans_advances")
    return render(request, "loan_form.html", {"form": form, "page_title": f"Edit Loan/Advance Request"})


@login_required
def loan_delete(request, pk):
    loan = get_object_or_404(LoanAdvanceRequest, pk=pk)
    if request.method == "POST":
        loan.delete()
        messages.success(request, "Loan/Advance request deleted successfully.")
        return redirect("loans_advances")
    return render(request, "loan_delete.html", {"loan": loan})


@login_required
def loan_approve(request, pk):
    loan = get_object_or_404(LoanAdvanceRequest, pk=pk)
    if request.method == "POST":
        loan.approval_status = "APPROVED"
        loan.approved_by = request.user
        if not loan.approved_amount:
            loan.approved_amount = loan.amount_requested
        loan.save()
        messages.success(request, "Loan/Advance request approved.")
        return redirect("loans_advances")
    return render(request, "loan_approve.html", {"loan": loan})


@login_required
def loan_reject(request, pk):
    loan = get_object_or_404(LoanAdvanceRequest, pk=pk)
    if request.method == "POST":
        loan.approval_status = "REJECTED"
        loan.approved_by = request.user
        loan.save()
        messages.success(request, "Loan/Advance request rejected.")
        return redirect("loans_advances")
    return render(request, "loan_reject.html", {"loan": loan})
