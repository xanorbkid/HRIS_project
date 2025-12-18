from django import forms
from .models import JobOpening, Applicant, Interview, Onboarding


class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = [
            "title",
            "department",
            "job_title",
            "employment_type",
            "location",
            "description",
            "requirements",
            "openings",
            "salary_range",
            "status",
            "closing_date",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.Select(attrs={"class": "form-select"}),
            "job_title": forms.Select(attrs={"class": "form-select"}),
            "employment_type": forms.Select(attrs={"class": "form-select"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "requirements": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "openings": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "salary_range": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "closing_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 3:
            raise forms.ValidationError("Job title must be at least 3 characters long.")
        return title


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            "job_opening",
            "first_name",
            "last_name",
            "email",
            "phone",
            "resume",
            "cover_letter",
            "experience_years",
            "skills",
            "source",
            "status",
        ]
        widgets = {
            "cover_letter": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            "applicant",
            "interviewer",
            "interview_type",
            "scheduled_date",
            "duration_minutes",
            "location",
            "feedback",
            "rating",
            "result",
        ]
        widgets = {
            "applicant": forms.Select(attrs={"class": "form-select"}),
            "interviewer": forms.Select(attrs={"class": "form-select"}),
            "interview_type": forms.Select(attrs={"class": "form-select"}),
            "scheduled_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control", "min": 15}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "feedback": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "rating": forms.NumberInput(attrs={"class": "form-control"}),
            "result": forms.Select(attrs={"class": "form-select"}),
        }


class OnboardingForm(forms.ModelForm):
    class Meta:
        model = Onboarding
        fields = [
            "employee",
            "task_name",
            "description",
            "assigned_to",
            "due_date",
            "status",
        ]
        widgets = {
            "employee": forms.Select(attrs={"class": "form-select"}),
            "task_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "assigned_to": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date:
            from django.utils import timezone
            if due_date < timezone.now().date():
                raise forms.ValidationError("Due date cannot be in the past.")
        return due_date
