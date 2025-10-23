from django.urls import path
from .views import *



urlpatterns = [
    # List / index of employees
    path('employee_list/', employee_list, name='employee_list'),
]