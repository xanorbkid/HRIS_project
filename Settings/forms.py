# Settings/forms.py
from django import forms

from .models import (
    Function,
    PermissionGroup,
    Responsibility,
    Role,
    Service,
    TypeOfService,
)

class FunctionForm(forms.ModelForm):
    class Meta:
        model = Function
        fields = ['name']

class TypeOfServiceForm(forms.ModelForm):
    class Meta:
        model = TypeOfService
        fields = ['name']

class ServiceForm(forms.ModelForm):
    LEVEL_CHOICES = [(i, f"Level {i}") for i in range(1, 11)]

    level = forms.TypedChoiceField(
        choices=LEVEL_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Service
        fields = ['name', 'type_of_service', 'level', 'parent_service']
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type_of_service": forms.Select(attrs={"class": "form-select"}),
            "parent_service": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            return name

        qs = Service.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("A service with this name already exists. Please choose another name.")
        return name

class ResponsibilityForm(forms.ModelForm):
    class Meta:
        model = Responsibility
        fields = ['name']


class PermissionGroupForm(forms.ModelForm):
    class Meta:
        model = PermissionGroup
        fields = ['name', 'description', 'permissions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description', 'is_active', 'permission_groups', 'permissions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
