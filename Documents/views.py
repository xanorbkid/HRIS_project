from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from .models import HRDocument, CompanyPolicy, ContractOrLetter
from .forms import HRDocumentForm, ContractOrLetterForm, CompanyPolicyForm


@login_required
def employee_documents(request):
    documents = HRDocument.objects.select_related("employee", "uploaded_by").all()
    return render(request, "employee_documents.html", {"documents": documents})


@login_required
def company_policies(request):
    policies = CompanyPolicy.objects.select_related("department", "uploaded_by").all()
    return render(request, "company_policies.html", {"policies": policies})


@login_required
def contracts_letters(request):
    contracts = ContractOrLetter.objects.select_related("employee", "issued_by").all()
    return render(request, "contracts_letters.html", {"contracts": contracts})



def upload_document(request):
    if request.method == "POST":
        form = HRDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("employee_documents")  # Adjust to your listing view name
    else:
        form = HRDocumentForm()

    return render(request, "upload_documents.html", {"form": form})

def generate_contract(request):
    if request.method == "POST":
        form = ContractOrLetterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("contracts_list")  # use your actual list page name
    else:
        form = ContractOrLetterForm()

    return render(request, "generate_contract.html", {"form": form})

def upload_policy(request):
    if request.method == "POST":
        form = CompanyPolicyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("policies_list")  # adjust if your list URL has a different name
    else:
        form = CompanyPolicyForm()

    return render(request, "policies/upload_policy.html", {"form": form})


