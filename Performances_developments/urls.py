from django.urls import path
from .views import *  # ✅ This must NOT be circular (views should not import urls)

# app_name = "performances_developments"

urlpatterns = [
    # path("reviews/", performance_reviews, name="performance_reviews"),
    path("goals/", goals, name="goals"),
    path("trainings/", training_programs, name="training_programs"),
       path("actions/", promotions_and_warnings, name="promotions_and_warnings"),
]
