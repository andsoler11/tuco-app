from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from apps.users.models import Profile
from .forms import CustomUserCreationForm
from utils.privacy import Privacy

privacy = Privacy()


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
        email_secured = privacy.secure_email(request.POST['email'].lower())
        username = email_secured['mask']
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
            email_secured = privacy.secure_email(user.email)
            user.username = email_secured['mask']
            user.email = email_secured['encrypted']
            user.email_mask = email_secured['mask']
            user.email_hash = email_secured['hash']

            phone = user.phone_number
            user.phone_number = privacy.encrypt(phone)
            user.phone_number_mask = Privacy.mask_phone_number(phone)
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