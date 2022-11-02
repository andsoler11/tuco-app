from django.contrib.auth.decorators import login_required
from multiprocessing import context
from django.shortcuts import render, redirect
from apps.dishes.models import Puppy
from django.contrib.auth.models import User


@login_required(login_url='login')
def listPets(request):
    page = 'pets'
    user_id = User.objects.get(username=request.user.username)
    pets = Puppy.objects.filter(owner_id=user_id)
    
    context = {
        'page': page, 
        'pets': pets
    }

    return render(request, 'list.html', context)


@login_required(login_url='login')
def deletePet(request, pk):
    pet = Puppy.objects.get(id=pk)

    if request.method == 'POST':
        # borramos de la BS y redireccionamos
        pet.delete()
        return redirect('list-pets')


def editPet(request, pk):
    pet = Puppy.objects.get(id=pk)
    context = {
        'pet': pet
    }
    return render(request, 'edit.html', context)
    
