from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'components/base.html')

def employee_list(request):
    # Logic to retrieve and display a list of employees
    return render(request, 'employee_list.html', {})