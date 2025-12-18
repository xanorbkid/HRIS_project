from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import  Goal, TrainingProgram, Promotion, Warning

# def performance_reviews(request):
#     reviews = PerformanceReview.objects.all()
#     return render(request, "performance_reviews.html", {"reviews": reviews})

@login_required
def goals(request):
    goals = Goal.objects.all()
    return render(request, "goals.html", {"goals": goals})

@login_required
def training_programs(request):
    trainings = TrainingProgram.objects.all()
    return render(request, "training_programs.html", {"trainings": trainings})

@login_required
def promotions_and_warnings(request):
    promotions = Promotion.objects.all()
    warnings = Warning.objects.all()
    return render(request, "promotions_and_warnings.html", {
        "promotions": promotions,
        "warnings": warnings,
    })
