from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.shortcuts import render, redirect
from accounts import forms
from accounts.models import User

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

def login_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('homepage')
    else:
        form = forms.LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('homepage')
    else:
        form = forms.SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('homepage')

@login_required
def profile_view(request):
    profile = User.objects.get(username=request.user)
    if request.method == 'POST':
        logout(request)

    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def change_photo_view(request):
    if request.method == 'POST':
        user = request.user
        user.profile_image = request.FILES['profile_new_image']
        user.save()
        return redirect('accounts:profile')
