from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from Employee.models import EmployeeProfile, PerformanceReview, EmployeeDocument
from Time_off_management.models import LeaveRequest, AttendanceRecord
from Time_off_management.forms import LeaveRequestForm
from Payroll.models import Payslip
from .forms import PersonalInfoForm, AvatarUploadForm, PasswordChangeCustomForm


def _get_or_create_employee(user):
    """Return the EmployeeProfile for the user, creating a shell profile if needed."""
    if not user.is_authenticated:
        return None

    employee = getattr(user, "employee_profile", None)
    if employee:
        return employee

    employee = EmployeeProfile.objects.select_related("user").filter(user=user).first()
    if employee:
        return employee

    # Restore soft-deleted profiles if present
    deleted_employee = EmployeeProfile.all_objects.filter(user=user).first()
    if deleted_employee:
        deleted_employee.restore()
        return deleted_employee

    join_date = user.date_joined.date() if user.date_joined else timezone.now().date()
    return EmployeeProfile.objects.create(
        user=user,
        date_joined=join_date,
        employment_type="full_time",
        status="active",
    )


@login_required
def my_profile(request):
    """Display logged-in user's profile if exists"""
    employee = _get_or_create_employee(request.user)

    # Get active tab (?tab=personal / ?tab=job / ?tab=documents / ?tab=security)
    tab = request.GET.get("tab", "personal")

    # Handle form submissions
    if request.method == "POST":
        if tab == "personal":
            # Update personal information
            form = PersonalInfoForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Personal information updated successfully.")
                return redirect("my_profile?tab=personal")
        elif tab == "security":
            # Change password
            form = PasswordChangeCustomForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password updated successfully.")
                return redirect("my_profile?tab=security")
        else:
            messages.error(request, "Invalid form submission.")
            form = None
    else:
        # Initialize forms for GET requests
        if tab == "personal":
            form = PersonalInfoForm(instance=request.user)
        elif tab == "security":
            form = PasswordChangeCustomForm(user=request.user)
        else:
            form = None

    return render(request, "my_profile.html", {
        "employee": employee,
        "tab": tab,
        "form": form,
    })


@login_required
@require_http_methods(["POST"])
def upload_avatar(request):
    """Handle avatar upload via AJAX"""
    form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
    if form.is_valid():
        form.save()
        return JsonResponse({
            "success": True,
            "message": "Profile photo updated successfully.",
            "avatar_url": request.user.profile_image.url if request.user.profile_image else None
        })
    return JsonResponse({
        "success": False,
        "message": "Failed to upload image. Please try again.",
        "errors": form.errors
    }, status=400)


@login_required
def download_cv(request):
    """Download CV document if available"""
    employee = _get_or_create_employee(request.user)
    if not employee:
        messages.error(request, "Unable to load your employee profile.")
        return redirect("my_profile")
    
    # Try to find a CV document
    cv_doc = EmployeeDocument.objects.filter(
        employee=employee,
        document_type__icontains="cv"
    ).first()
    
    if not cv_doc:
        cv_doc = EmployeeDocument.objects.filter(
            employee=employee,
            document_type__icontains="resume"
        ).first()
    
    if cv_doc and cv_doc.file:
        # Determine content type based on file extension
        file_extension = cv_doc.file.name.split('.')[-1].lower()
        content_types = {
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain',
        }
        content_type = content_types.get(file_extension, 'application/octet-stream')
        
        response = HttpResponse(cv_doc.file.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{cv_doc.document_type}.{file_extension}"'
        return response
    
    messages.warning(request, "No CV document found. Please upload one in the Documents section.")
    return redirect("my_profile?tab=documents")



@login_required
def my_attendance(request):
    """Show personal attendance records"""
    employee = _get_or_create_employee(request.user)

    attendance = AttendanceRecord.objects.filter(employee=employee).order_by("-date")
    return render(request, "my_attendance.html", {"attendance": attendance})


@login_required
def my_leave_requests(request):
    employee = _get_or_create_employee(request.user)
    leaves = LeaveRequest.objects.filter(employee=employee).order_by("-created_at")
    form = LeaveRequestForm()

    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            if end_date < start_date:
                form.add_error("end_date", "End date cannot be before start date.")
            else:
                total_days = Decimal((end_date - start_date).days + 1)
                leave_request = form.save(commit=False)
                leave_request.employee = employee
                leave_request.total_days = total_days
                leave_request.created_by = request.user
                leave_request.save()
                leave_request.submit(request.user)
                messages.success(request, "Leave request submitted for approval.")
                return redirect("my_leave_requests")
        else:
            messages.error(request, "Please fix the errors in the form.")

    return render(request, "my_leave_requests.html", {
        "leaves": leaves,
        "form": form,
    })


@login_required
def my_payslips(request):
    """Show payslips of logged-in user"""
    employee = _get_or_create_employee(request.user)

    payslips = Payslip.objects.filter(
        payroll_record__employee=employee
    ).select_related(
        "payroll_record__batch"
    ).order_by(
        "-payroll_record__batch__pay_period_end"
    )
    return render(request, "my_payslips.html", {"payslips": payslips})


@login_required
def my_performance(request):
    employee = _get_or_create_employee(request.user)
    reviews = PerformanceReview.objects.filter(employee=employee) if employee else []
    return render(request, "my_performance.html", {"reviews": reviews, "employee": employee})


@login_required
def account_settings(request):
    stored_settings = request.session.get(
        "account_settings",
        {
            "theme": "light",
            "notifications": "email",
        },
    )

    if request.method == "POST":
        stored_settings = {
            "theme": request.POST.get("theme", "light"),
            "notifications": request.POST.get("notifications", "email"),
        }
        request.session["account_settings"] = stored_settings
        messages.success(request, "Account settings updated.")
        return redirect("account_settings")

    return render(request, "account_settings.html", {"settings": stored_settings})
