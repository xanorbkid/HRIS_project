from django.urls import path
from .views import *

urlpatterns = [
    path('job_openings/', job_openings, name='job_openings'),
    path('applicants/', applicants, name='applicants'),
    path('interviews/', interviews, name='interviews'),
    path('onboarding/', onboarding, name='onboarding'),

    path("applicants/", applicant_list, name="applicant-list"),
    path("applicants/add/", applicant_create, name="applicant-create"),
    path("applicants/<int:pk>/", applicant_detail, name="applicant-detail"),
    path("applicants/<int:pk>/edit/", applicant_edit, name="applicant-edit"),
    path("applicants/<int:pk>/delete/", applicant_delete, name="applicant-delete"),

    path("jobs/add/", job_create, name="job-create"),
    path("jobs/<int:pk>/", job_detail, name="job-detail"),
    path("jobs/<int:pk>/edit/", job_edit, name="job-edit"),
    path("jobs/<int:pk>/delete/", job_delete, name="job-delete"),
    path("jobs/", job_list, name="job-list"),

    path("interviews/", interview_list, name="interview-list"),
    path("interviews/add/", interview_create, name="interview-create"),
    path("interviews/<int:pk>/edit/", interview_edit, name="interview-edit"),
    path("interviews/<int:pk>/", interview_detail, name="interview-detail"),
    path("interviews/<int:pk>/delete/", interview_delete, name="interview-delete"),

    path("onboarding/", onboarding_list, name="onboarding-list"),
    path("onboarding/add/", onboarding_create, name="onboarding-create"),
    path("onboarding/<int:pk>/", onboarding_detail, name="onboarding-detail"),
    path("onboarding/<int:pk>/edit/", onboarding_edit, name="onboarding-edit"),
    path("onboarding/<int:pk>/delete/", onboarding_delete, name="onboarding-delete"),

]
