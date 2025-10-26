
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


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path('auth/', include('Auth.urls')),
    path('employee/', include('Employee.urls')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

