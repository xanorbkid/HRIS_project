# documents/forms.py

from django import forms
from .models import HRDocument, ContractOrLetter, CompanyPolicy

class HRDocumentForm(forms.ModelForm):
    class Meta:
        model = HRDocument
        fields = ["employee", "document_type", "title", "file", "expiry_date"]


class ContractOrLetterForm(forms.ModelForm):
    class Meta:
        model = ContractOrLetter
        fields = '__all__'

class CompanyPolicyForm(forms.ModelForm):
    class Meta:
        model = CompanyPolicy
        fields = [
            "title",
            "category",
            "description",
            "file",
            "effective_date",
            "department",
        ]