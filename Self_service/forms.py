from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


class PersonalInfoForm(forms.ModelForm):
    """Form for updating personal information"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-pill px-3'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-pill px-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill px-3'}),
            'phone': forms.TextInput(attrs={'class': 'form-control rounded-pill px-3'}),
        }


class AvatarUploadForm(forms.ModelForm):
    """Form for uploading profile image"""
    
    class Meta:
        model = User
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'avatar-upload-input',
                'style': 'display: none;'
            })
        }


class PasswordChangeCustomForm(PasswordChangeForm):
    """Custom password change form with styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control rounded-pill px-3',
            'placeholder': 'Current Password'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control rounded-pill px-3',
            'placeholder': 'New Password'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control rounded-pill px-3',
            'placeholder': 'Confirm New Password'
        })

