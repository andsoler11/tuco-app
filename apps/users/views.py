from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from apps.users.models import Profile
import hashlib
from .forms import CustomUserCreationForm
from pprint import pprint

def renderHomepage(request):
    """Render the homepage"""
    context = {'page': 'homepage'}
    return render(request, 'homepage.html', context)


def userLogin(request):
    """function to login a user"""
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('dishes')

    if request.method == 'POST':
        username = request.POST['email'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'Username doest not exist')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dishes')
        else:        
            messages.error(request, 'username or password is incorrect')
 
    return render(request, 'users/login_register.html', context)


def registerUser(request):
    """Registros de usuario"""
    page = 'register'
    form = CustomUserCreationForm

    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.lower()
            user.email = user.email.lower()
            user.save()

            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('dishes')

        else:
            for msg in form.errors:
                messages.error(request, f"{form.errors[msg]}")
    

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def recoverPassword(request):
    """Render recover password page"""
    page = 'recoverPassword'
    context = {'page': 'recoverPassword'}
    return render(request, 'users/login_register.html', context)

def newPassword(request):
    """Render new password page"""
    page = 'newPassword'
    context = {'page': 'newPassword'}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logout')
    return redirect('login')


def profile(request):
    """Render user dashboard"""
    context = {'page': 'profile'}
    return render(request, 'users/dashboard.html', context)

def account(request):
    """Render My Data page"""
    context = {'page': 'account'}
    return render(request, 'users/account.html', context)