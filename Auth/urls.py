from django.urls import path
from .views import *



urlpatterns = [
    # List / index of employees
   path('login/', login_view, name='login'),
]