
from django.contrib import admin

"""
URL Configuration for HRIS Project
This module defines the main URL patterns for the Human Resource Information System (HRIS).
It includes routes for admin interface, authentication, and employee management.
URL Patterns:
    - admin/: Django admin interface
    - auth/: Authentication related URLs
    - employee/: Employee management related URLs
The static() helper is used to serve media files during development.
Note:
    Make sure DEBUG=True only in development environment when using static()
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Employee.views import *
from Time_off_management.views import *
from Auth.views import dashboard, dashboard_export, workforce_report


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", dashboard, name="dashboard"),
    path('auth/', include('Auth.urls')),
    path('employee/', include('Employee.urls')),
    path ('time_off/', include('Time_off_management.urls')),
    path ('recruitment/', include('Recruitment.urls')),
    path ('payroll/', include('Payroll.urls')),
    path ('performance_management/', include('Performances_developments.urls')),
    path ('documents/', include('Documents.urls')),
    path ('self_service/', include('Self_service.urls')),
    path('support_others/', include(('Support_others.urls', 'support'), namespace='support')),
    path('settings/', include('Settings.urls')),
    path("dashboard/export/", dashboard_export, name="dashboard_export"),
    path(
        "dashboard/workforce-report/", workforce_report, name="workforce_report"
    ),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
