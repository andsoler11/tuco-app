from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from apps.users.models import CustomUser
from .forms import CustomUserCreationForm
from utils.privacy import Privacy
from django.contrib.auth.decorators import login_required
from apps.users.utils import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        username = request.POST['email'].lower()
        password = request.POST['password']

        try:    
            user = CustomUser.objects.get(username=username)
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
    if request.method == 'POST':
        requested_email = request.POST['email'].lower()
        try:
            user = CustomUser.objects.get(email_hash=privacy.hash_string(requested_email))
        except:
            messages.error(request, 'El email no existe')
            return redirect('recover-password')
        
        if send_recovery_email(request, requested_email):
            messages.error(request, f'Ha ocurrido un error al enviar el correo electrónico')
            return redirect('recover-password')

        messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para recuperar tu contraseña')

    context = {'page': 'recoverPassword'}
    return render(request, 'users/login_register.html', context)


def newPassword(request):
    """Render new password page"""
    if request.method == 'POST':
        actual_password = request.POST.get('actual_password')
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if actual_password and not request.user.check_password(actual_password):
            messages.error(request, 'La contraseña actual no es correcta')
            return redirect('new-password')

        if password == confirm_password:
            if not validate_password(request, password):
                return redirect('new-password')
            user = CustomUser.objects.get(id=request.user.id)
            user.set_password(password)
            user.save()
            login(request, user)
            messages.success(request, 'contraseña actualizada')
            return redirect('profile')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('new-password')

    if request.GET.get('token'):
        reset_token = request.GET.get('token')
        email = cache.get(reset_token)

        if not email:
            # Reset token is invalid or expired
            messages.error(request, 'Invalid or expired reset token.')
            return redirect('recover-password')
    

        user = CustomUser.objects.get(email_hash=privacy.hash_string(email))
        if user is None:
            messages.error(request, 'Invalid or expired reset token.')
            return redirect('recover-password')

        context = {'page': 'newPassword', 'email': email}
        return render(request, 'users/login_register.html', context)
            
    context = {'page': 'newPassword'}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logout')
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    """Render user dashboard"""
    user_data = CustomUser.objects.get(id=request.user.id)
    if user_data.full_name:
        user_data.full_name = privacy.decrypt(user_data.full_name)
    context = {'page': 'profile', 'user_data': user_data}
    return render(request, 'users/dashboard.html', context)

@login_required(login_url='login')
def account(request):
    """Render My Data page"""
    user_data = CustomUser.objects.get(id=request.user.id)

    if request.method == 'POST':
        name = request.POST['name']
        if len(name) > 50:
            messages.error(request, 'Name is too long')
            return redirect('account')
        
        if len(name) < 3:
            messages.error(request, 'Name is too short')
            return redirect('account')

        if not name.replace(" ", "").isalpha():
            messages.error(request, 'Name is not valid')
            return redirect('account')

        user_data.full_name = privacy.encrypt(request.POST['name'])
        user_data.phone_number = privacy.encrypt(request.POST['phone'])
        user_data.phone_number_mask = Privacy.mask_phone_number(request.POST['phone'])
        user_data.save()
        messages.success(request, 'User data was updated')

    user_data.email = privacy.decrypt(user_data.email)
    user_data.full_name = privacy.decrypt(user_data.full_name)
    user_data.phone_number = privacy.decrypt(user_data.phone_number)
    context = {'page': 'account', 'user_data': user_data}
    return render(request, 'users/account.html', context)
