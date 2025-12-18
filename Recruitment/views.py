from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import JobOpening, Applicant, Interview, Onboarding, JobOffer
from .forms import ApplicantForm, JobOpeningForm, InterviewForm, OnboardingForm

def _render_job_openings(request):
    jobs = JobOpening.objects.select_related('department', 'job_title').all().order_by("-posted_date")
    return render(
        request,
        'job_openings.html',
        {
            'page_title': 'Job Openings',
            'jobs': jobs,
            'job_openings': jobs,
            'job_form': JobOpeningForm(),
        },
    )


@login_required
def job_openings(request):
    return _render_job_openings(request)



@login_required
def applicants(request):
    applicants = Applicant.objects.select_related('job_opening').all()
    context = {
        'page_title': 'Applicants / Candidates',
        'applicants': applicants,
    }
    return render(request, 'applicants.html', context)


def _render_interviews(request):
    interview_qs = Interview.objects.select_related('applicant', 'interviewer').all().order_by("-scheduled_date")
    return render(
        request,
        'interviews.html',
        {
            'page_title': 'Interviews & Hiring',
            'interviews': interview_qs,
            'interview_form': InterviewForm(),
        },
    )


@login_required
def interviews(request):
    return _render_interviews(request)


def _render_onboarding(request):
    tasks = Onboarding.objects.select_related('employee', 'assigned_to').all().order_by("due_date")
    return render(
        request,
        'onboarding.html',
        {
            'page_title': 'Onboarding',
            'tasks': tasks,
            'onboarding_tasks': tasks,
            'onboarding_form': OnboardingForm(),
        },
    )


@login_required
def onboarding(request):
    return _render_onboarding(request)

@login_required
def applicant_list(request):
    applicants = Applicant.objects.all()
    return render(request, "list.html", {"applicants": applicants})

def applicant_create(request):
    form = ApplicantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("applicant-list")
    return render(request, "form.html", {"form": form})

def applicant_edit(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    form = ApplicantForm(request.POST or None, instance=applicant)
    if form.is_valid():
        form.save()
        return redirect("applicant-list")
    return render(request, "form.html", {"form": form})

def applicant_detail(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    return render(request, "detail.html", {"applicant": applicant})

def applicant_delete(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    applicant.delete()
    return redirect("applicant-list")

@login_required
@require_POST
def job_create(request):
    form = JobOpeningForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Job opening created successfully.")
    else:
        messages.error(request, "Failed to create job opening. Please review the form and try again.")
    return redirect("job-list")

@login_required
@require_POST
def job_edit(request, pk):
    job = get_object_or_404(JobOpening, pk=pk)
    form = JobOpeningForm(request.POST, instance=job)
    if form.is_valid():
        form.save()
        messages.success(request, "Job opening updated successfully.")
    else:
        messages.error(request, "Failed to update job opening.")
    return redirect("job-list")

@login_required
def job_list(request):
    return _render_job_openings(request)


def job_detail(request, pk):
    job = get_object_or_404(JobOpening, pk=pk)
    return render(request, "job_detail.html", {"job": job})

# DELETE
@login_required
@require_POST
def job_delete(request, pk):
    job = get_object_or_404(JobOpening, pk=pk)
    job.delete()
    messages.success(request, "Job opening deleted.")
    return redirect("job-list")

@login_required
def interview_list(request):
    return _render_interviews(request)

@login_required
@require_POST
def interview_create(request):
    form = InterviewForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Interview scheduled successfully.")
    else:
        messages.error(request, "Failed to schedule interview.")
    return redirect("interview-list")

@login_required
@require_POST
def interview_edit(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    form = InterviewForm(request.POST, instance=interview)
    if form.is_valid():
        form.save()
        messages.success(request, "Interview updated successfully.")
    else:
        messages.error(request, "Failed to update interview.")
    return redirect("interview-list")

def interview_detail(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    return render(request, "interview_detail.html", {"interview": interview})

@login_required
@require_POST
def interview_delete(request, pk):
    interview = get_object_or_404(Interview, pk=pk)
    interview.delete()
    messages.success(request, "Interview deleted.")
    return redirect("interview-list")

@login_required
def onboarding_list(request):
    return _render_onboarding(request)

# CREATE
@login_required
@require_POST
def onboarding_create(request):
    form = OnboardingForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Onboarding task created successfully.")
    else:
        messages.error(request, "Failed to create onboarding task.")
    return redirect("onboarding-list")

# DETAIL
def onboarding_detail(request, pk):
    task = get_object_or_404(Onboarding, pk=pk)
    return render(request, "onboarding_detail.html", {"task": task})

# EDIT
@login_required
@require_POST
def onboarding_edit(request, pk):
    task = get_object_or_404(Onboarding, pk=pk)
    form = OnboardingForm(request.POST, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, "Onboarding task updated successfully.")
    else:
        messages.error(request, "Failed to update onboarding task.")
    return redirect("onboarding-list")

# DELETE
@login_required
@require_POST
def onboarding_delete(request, pk):
    task = get_object_or_404(Onboarding, pk=pk)
    task.delete()
    messages.success(request, "Onboarding task deleted.")
    return redirect("onboarding-list")
