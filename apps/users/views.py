from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from apps.users.models import Profile
import hashlib
from .forms import CustomUserCreationForm

# def userLogin(request):
#     page    = 'login'
#     context = {'page': page}
#     if request.method == 'POST':
#         email = request.POST['email'].lower()
#         password = request.POST['password']
#         pass_encoded = password.encode()
#         pass_hashed = hashlib.sha256(pass_encoded)

#         try:
#             user_data = Profile.objects.get(email=email)
#         except:
#             messages.error(request, 'Username doest not exist')

#         if pass_hashed.hexdigest() == user_data.password:
#             login(request, user_data)
#             return redirect('register')
#         else:
#             messages.error(request, 'username or password is incorrect')
        
#     return render(request, 'users/login.html', context)


def userLogin(request):
    """function to login a user"""
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('register')

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
            messages.error(request, 'An error has occurred during registration')
    

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)



# def registerUser(request):
#     page = 'register'
    
#     if request.method == 'POST': 
#         email = request.POST['email'].lower()
#         password = request.POST['password'] 
#         pass_encoded = password.encode()
#         pass_hashed = hashlib.sha256(pass_encoded)

#         try:
#             Profile.objects.create(email=email, password=pass_hashed.hexdigest())

#             # sacamos el mensaje, logeamos al usuario y redireccionamos
#             messages.success(request, 'User account was created!')
#             return redirect('login')
#         except:
#             messages.error(request, 'An error has occurred during registration')

#     context = {'page': page}
#     return render(request, 'users/login.html', context)



def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logout')
    return redirect('login')
