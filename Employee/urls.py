from django.urls import path
from .views import *



urlpatterns = [
    # List / index of employees
    path('', home, name='employee_home'),
    path('employee_list/', employee_list, name='employee_list'),
    path('department_list/', department_list, name='department_list'),
]