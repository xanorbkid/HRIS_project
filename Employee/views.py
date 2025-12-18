from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import DepartmentForm, JobTitleForm, EmployeeProfileForm

# Create your views here.
# def dashboard(request):
#     return render(request, 'dashboard.html')

def employee_list(request):
    employees_qs = EmployeeProfile.objects.select_related('user', 'department', 'job_title')
    search_query = request.GET.get("q", "").strip()
    if search_query:
        employees_qs = employees_qs.filter(
            Q(user__first_name__icontains=search_query)
            | Q(user__last_name__icontains=search_query)
            | Q(user__username__icontains=search_query)
            | Q(user__email__icontains=search_query)
            | Q(department__name__icontains=search_query)
            | Q(job_title__name__icontains=search_query)
        )
    paginator = Paginator(employees_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'Employee List',
        'employees': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'employee_form': EmployeeProfileForm(),
    }

    return render(request, 'employee.html', context)


@login_required
def employee_create(request):
    form = EmployeeProfileForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Employee created successfully.")
            return redirect("employee_list")

    return render(request, "form.html", {
        "page_title": "Add Employee",
        "form": form,
    })


@login_required
def employee_edit(request, pk):
    employee = get_object_or_404(EmployeeProfile, pk=pk)
    form = EmployeeProfileForm(request.POST or None, instance=employee)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect("employee_list")

    return render(request, "form.html", {
        "page_title": f"Edit Employee - {employee}",
        "form": form,
    })


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(
        EmployeeProfile.objects.select_related('user', 'department', 'job_title', 'manager'),
        pk=pk
    )
    return render(request, "employee_detail.html", {
        "page_title": f"Employee - {employee}",
        "employee": employee,
    })


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(EmployeeProfile, pk=pk)

    if request.method == "POST":
        employee.delete()
        messages.success(request, "Employee deleted successfully.")
        return redirect("employee_list")

    return render(request, "employee_delete.html", {
        "page_title": "Delete Employee",
        "item": employee,
    })

def department_list(request):
    departments_qs = Department.objects.all()
    search_query = request.GET.get("q", "").strip()
    if search_query:
        departments_qs = departments_qs.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    paginator = Paginator(departments_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'Department List',
        'departments': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'department_form': DepartmentForm(),
    }
    return render(request, 'department.html', context)


def department_add(request):
    form = DepartmentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Department created successfully.")
            return redirect("department_list")

    return render(request, "department_add.html", {
        "page_title": "Add Department",
        "form": form
    })

@login_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=department)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully.")
            return redirect("department_list")

    return render(request, "department_edit.html", {
        "page_title": "Edit Department",
        "form": form,
        "item": department
    })


def department_view(request, pk):
    department = get_object_or_404(Department, pk=pk)

    return render(request, "department_view.html", {
        "page_title": f"Department - {department.name}",
        "item": department
    })

@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        department.delete()
        messages.success(request, "Department deleted successfully.")
        return redirect("department_list")

    return render(request, "department_delete.html", {
        "page_title": "Delete Department",
        "item": department
    })

def jobtitle_list(request):
    jobtitles_qs = JobTitle.objects.prefetch_related('employeeprofile_set').all()
    search_query = request.GET.get("q", "").strip()
    if search_query:
        jobtitles_qs = jobtitles_qs.filter(
            Q(name__icontains=search_query)
            | Q(level__icontains=search_query)
            | Q(description__icontains=search_query)
        )
    paginator = Paginator(jobtitles_qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'Job Titles',
        'jobtitles': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'jobtitle_form': JobTitleForm(),
    }

    return render(request, 'jobtitle.html', context)


@login_required
def jobtitle_view(request, pk):
    jobtitle = get_object_or_404(JobTitle.objects.prefetch_related('employeeprofile_set'), pk=pk)
    return render(request, 'jobtitle_view.html', {
        'page_title': f"Job Title - {jobtitle.name}",
        'jobtitle': jobtitle,
    })

# return modal with form (GET) or process creation (POST)
@login_required
@permission_required('employee.add_jobtitle', raise_exception=True)
def jobtitle_create(request):
    form = JobTitleForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Job title created successfully.")
            return redirect("jobtitle_list")
    return render(request, 'jobtitle_form.html', {'form': form, 'page_title': 'Add Job Title'})

@login_required
@permission_required('employee.change_jobtitle', raise_exception=True)
def jobtitle_edit(request, pk):
    obj = get_object_or_404(JobTitle, pk=pk)
    form = JobTitleForm(request.POST or None, instance=obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Job title updated successfully.")
            return redirect("jobtitle_list")
    return render(request, 'jobtitle_form.html', {'form': form, 'page_title': f"Edit Job Title - {obj.name}", 'jobtitle': obj})

@login_required
@permission_required('employee.delete_jobtitle', raise_exception=True)
def jobtitle_delete(request, pk):
    obj = get_object_or_404(JobTitle, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Job title deleted.")
        return redirect("jobtitle_list")
    return render(request, 'jobtitle_confirm_delete.html', {'jobtitle': obj})


def organization_chart(request):
    departments = Department.objects.prefetch_related('employeeprofile_set').all()
    data = {dept: list(dept.employeeprofile_set.all()) for dept in departments}

    context = {
        'page_title': 'Organization Chart',
        'departments': data,
    }
    return render(request, 'organization_chart.html', context)
