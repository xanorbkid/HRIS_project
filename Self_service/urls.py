from django.urls import path
from .views import *

# app_name = "SelfService"

urlpatterns = [
    path("my-profile/", my_profile, name="my_profile"),
    path("my-profile/upload-avatar/", upload_avatar, name="upload_avatar"),
    path("my-profile/download-cv/", download_cv, name="download_cv"),
    path("my-attendance/", my_attendance, name="my_attendance"),
    path("my-leave-requests/", my_leave_requests, name="my_leave_requests"),
    path("my-payslips/", my_payslips, name="my_payslips"),
    path("my-performance/", my_performance, name="my_performance"),
    path("account-settings/", account_settings, name="account_settings"),
]
