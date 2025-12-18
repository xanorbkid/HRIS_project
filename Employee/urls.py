from django.urls import path, re_path
from .views import *



urlpatterns = [
    # List / index of employees
    # path('', dashboard, name='employee_home'),
    path('employee_list/', employee_list, name='employee_list'),
    path('employees/add/', employee_create, name='employee_create'),
    path('employees/<int:pk>/', employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', employee_delete, name='employee_delete'),

    path('department_list/', department_list, name='department_list'),
    path("departments/", department_list, name="department_list"),
    path("departments/add/", department_add, name="department_add"),
    path("departments/<int:pk>/", department_view, name="department_view"),
    path("departments/<int:pk>/edit/", department_edit, name="department_edit"),
    path("departments/<int:pk>/delete/", department_delete, name="department_delete"),

    path('jobtitle_list/', jobtitle_list, name='jobtitle_list' ),
    path('jobtitles/add/', jobtitle_create, name='jobtitle_create'),
    path('jobtitles/<int:pk>/', jobtitle_view, name='jobtitle_view'),
    path('jobtitles/<int:pk>/edit/', jobtitle_edit, name='jobtitle_edit'),
    path('jobtitles/<int:pk>/delete/', jobtitle_delete, name='jobtitle_delete'),
    
    path('organization_chart/', organization_chart, name='organization_chart'),
]