from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request, 'about.html')

def rules(request):
    return render(request, 'rules.html')