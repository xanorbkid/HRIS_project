from django import forms

from .models import LeaveRequest, Holiday, AttendanceRecord


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "reason"]
        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "reason": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional note"}),
        }


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ["name", "date", "country", "is_recurring", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Holiday name"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional country"}),
            "is_recurring": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional description"}),
        }


class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = [
            "employee",
            "date",
            "shift",
            "check_in",
            "check_out",
            "status",
            "worked_hours",
            "overtime_hours",
            "notes",
        ]
        widgets = {
            "employee": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "shift": forms.Select(attrs={"class": "form-select"}),
            "check_in": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "check_out": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "worked_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.25", "min": "0"}),
            "overtime_hours": forms.NumberInput(attrs={"class": "form-control", "step": "0.25", "min": "0"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional note"}),
        }
