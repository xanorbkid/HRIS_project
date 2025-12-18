from django import forms
from .models import Deduction, Benefit, LoanAdvanceRequest, PayrollBatch, SalaryStructure, SalaryComponent
from Employee.models import EmployeeProfile


class DeductionForm(forms.ModelForm):
    class Meta:
        model = Deduction
        fields = ['name', 'description', 'default_amount']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'default_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class BenefitForm(forms.ModelForm):
    class Meta:
        model = Benefit
        fields = ['name', 'description', 'taxable', 'default_value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'taxable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'default_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class LoanAdvanceRequestForm(forms.ModelForm):
    class Meta:
        model = LoanAdvanceRequest
        fields = ['employee', 'request_type', 'amount_requested', 'reason', 'repayment_months']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'request_type': forms.Select(attrs={'class': 'form-select'}),
            'amount_requested': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'repayment_months': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PayrollBatchForm(forms.ModelForm):
    class Meta:
        model = PayrollBatch
        fields = ['batch_name', 'pay_period_start', 'pay_period_end']
        widgets = {
            'batch_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pay_period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pay_period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SalaryStructureForm(forms.ModelForm):
    components = forms.ModelMultipleChoiceField(
        queryset=SalaryComponent.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = SalaryStructure
        fields = ['name', 'components']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

