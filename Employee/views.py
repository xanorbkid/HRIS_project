from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return render(request, 'dashboard.html')

def employee_list(request):
    # Retrieve active employee profiles and pass them to the template
    

    employees = EmployeeProfile.objects.select_related('user', 'department', 'job_title').all()

    context = {
        'page_title': 'Employee List',
        'employees': employees,
    }

    return render(request, 'employee.html', context)

def department_list(request):
    departments = Department.objects.all()

    context = {
        'page_title': 'Department List',
        'departments': departments,
    }
    return render(request, 'department.html', context)