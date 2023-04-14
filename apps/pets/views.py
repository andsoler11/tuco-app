from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.dishes.models import Pet, Menus
from django.contrib.auth.models import User


@login_required(login_url='login')
def listPets(request):
    page = 'pets'
    user_id = User.objects.get(username=request.user.username)
    pets = Pet.objects.filter(owner_id=user_id).order_by('name')

    for pet in pets:
        if pet.menu_id is not None:
            pet.menu = Menus.objects.get(id=pet.menu_id)
    
    context = {
        'page': page, 
        'pets': pets
    }

    return render(request, 'list.html', context)


@login_required(login_url='login')
def deletePet(request, pk):
    pet = Pet.objects.get(id=pk)

    if request.method == 'POST':
        pet.delete()
        return redirect('list-pets')
    

def editPetMenu(request, pk):
    pet = Pet.objects.get(id=pk)
    
    menus = Menus.objects.all()
    if request.method == 'POST':
        menu_id = request.POST.get('menu')
        menu = Menus.objects.get(id=menu_id)
        pet.menu_id = menu.id
        pet.save()
        return redirect('list-pets')

    context = {
        'pet': pet,
        'menus': menus
    }

    return render(request, 'menu-edit.html', context)