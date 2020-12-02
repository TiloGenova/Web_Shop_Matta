from django.shortcuts import render
#from .models import Activity, Contact

# Create your views here.


def home(request):
    return render(request, 'home.html', {})


def base(request):
    return render(request, 'base.html', {'home': home})