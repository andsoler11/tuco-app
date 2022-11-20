from pprint import pprint
from django.contrib.auth.decorators import login_required
import string
from unicodedata import name
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Breeds, Puppy, ContactDetail, Menus
from .forms import PuppyForm, MenusForm
from .utils import *
import json
import os
import re
YOUNG_AGE = 2
MIDDLE_AGE = 4
ADULT_AGE = 8

puppy_ages = {
    'small': 11,
    'medium': 12,
    'large': 18,
    'giant': 24
}



def dishesHome(request):
    page = 'multistep-form'
    form = PuppyForm()
    points = 0
    grams = 0
    grams_percent = 0
    dish = ''
    user = None

    if request.method == 'POST':
        activity_level_input        = request.POST.get('activity_level')
        reproductive_state_input    = request.POST.get('reproductive_state')
        body_image_input            = request.POST.get('body_image')

        age, age_type    = validate_age_inputs(request.POST.get('age'), request.POST.get('age_type'))     
        weight           = format_weight(request.POST.get('weight'))

        # get the data!
        grams, grams_percent, points = determineGrams(
            activity_level=activity_level_input, 
            reproductive_state=reproductive_state_input, 
            body_image=body_image_input, 
            weight=weight,
            age_type=age_type,
            age=age
        )


        ################ section for user contact ################
        if request.POST.get('name_contact') and request.POST.get('email_contact'):
            email = request.POST.get('email_contact').lower()
            name = request.POST.get('name_contact').lower()
            
            if not '@' in email:
                return render(request, 'dishes/dishes-home.html', {'page': page, 'form': form, 'error': 'El email no es valido'})

            user = User.objects.get(username=email)
            if user is None:
                user = User(
                    username=email,
                    email=email,
                    first_name=name,
                )
                user.save()

        if user is not None:
            user_upload = user
        else:
            user_upload = request.user
        ##########################################################



        puppy = Puppy(
            owner=user_upload, 
            name=request.POST.get('name'), 
            age=age,
            body_image=body_image_input,
            reproductive_state=reproductive_state_input,
            activity_level=activity_level_input,
            allergies=request.POST.get('allergies'),
            special_needs=request.POST.get('special_needs'),
            breed=request.POST.get('breed'),
            weight=weight,
            grams=grams,
            grams_percent=grams_percent,
            points=points,
            is_barf_active=request.POST.get('natural_food')
        )
        puppy.save()
        pk = puppy.id



        ################ section for user contact ################
        if request.POST.get('name_contact') and request.POST.get('email_contact'):
            contact = ContactDetail(
                    name_contact=name,
                    email_contact=email,
                    pet=puppy
                )
            contact.save()
        ##########################################################

        return redirect('menus', pk=pk)

    breeds = Breeds.objects.all()

    context = {
        'page': page, 
        'dish': dish, 
        'form': form, 
        'grams': grams, 
        'grams_percent': grams_percent, 
        'points': points, 
        'breeds':breeds
    }

    return render(request, 'dishes/home.html', context)


# @login_required(login_url='login')
def menusHome(request, pk):
    page = 'menus'
    puppy_data = Puppy.objects.get(id=pk)
    available_menus = Menus.objects.all()
    grams = puppy_data.grams
    food = puppy_data.is_barf_active
    allergies = puppy_data.allergies
    special_needs = puppy_data.special_needs
    weight = puppy_data.weight

    # mind using sessions in the future
    # food_type = request.session['food_type']

    # get the percents for each type of ingredient
    percent_ingredients = get_ingredients_percent(grams)

    # round the final grams
    grams = round(grams)

    if food == 'no':
        percent_ingredients = get_ingredients_percent(grams, 'no')

        week_percents = {
            'Primera semana': {},
            'Segunda semana': {},
            'Tercera semana': {}
        }

        total_grams = 0
        for k,v in percent_ingredients.items():
            week_percents['Primera semana'][k] = round(v/2)
            week_percents['Segunda semana'][k] = round(v/1.5)
            week_percents['Tercera semana'][k] = v
            total_grams += round(v/2) + round(v/1.5) + v

        # round the final grams
        grams = round(total_grams)

    
    percents_data = get_percents_data(grams, percent_ingredients)
    

    if (weight < 10):
        price = 1432
    elif (weight >= 10 and weight < 25):
        price = 1382
    elif (weight >= 25 and weight < 40):
        price = 1333
    elif weight >= 40:
        price = 1284

    price_grams = round((grams / 110) * price)
    
    context = {
        'page': page, 
        'grams': grams, 
        'puppy_data': puppy_data,
        'percent_ingredients': percents_data, 
        'grams_ingredients': percent_ingredients, 
        'price_grams': price_grams,
        'allergies': allergies,
        'special_needs': special_needs,
        'available_menus': available_menus,
    }

    if food == 'no':
        context['week_percents'] = week_percents

    return render(request, 'dishes/menus.html', context)



def editPet(request, pk):
    puppy = Puppy.objects.get(id=pk)
    form = PuppyForm(instance=puppy)

    if request.method == 'POST':
        puppy.delete()
        return dishesHome(request)

    context = {'puppy':puppy, 'page': 'edit-pet', 'form': form}

    return render(request, 'dishes/edit-pet.html', context)


def createMenu(request):
    form = MenusForm()

    if request.method == 'POST':
        percents_array = convert_string_to_array(request.POST.get('percents'))
        nutrition_data = convert_string_to_array(request.POST.get('nutrition_information'))

        menu = Menus(
            name=request.POST.get('name'),
            percents=json.dumps(percents_array),
            description=request.POST.get('description'),
            ingredients_description=request.POST.get('ingredients_description'),
            nutrition_information=json.dumps(nutrition_data),
        )
        menu.save()
        return redirect('menus-list')

    context = {'form':form, 'page': 'create-menu'}
    return render(request, 'menus/create-menu.html', context)


def listMenus(request):
    menus = Menus.objects.all()
    context = {'menus':menus, 'page': 'menus-list'}
    return render(request, 'menus/menus-list.html', context)



def deleteMenu(request, pk):
    menu = Menus.objects.get(id=pk)

    if request.method == 'POST':
        # borramos de la BS y redireccionamos
        menu.delete()
        return redirect('menus-list')


def updateMenu(request, pk):
    menu = Menus.objects.get(id=pk)
    
    if request.method == 'POST':
        menu.delete()
        return createMenu(request)


    menu.percents = convert_json_to_string(menu.percents)
    menu.nutrition_information = convert_json_to_string(menu.nutrition_information)

    form = MenusForm(instance=menu)
    context = {'menu':menu, 'page': 'update-menu', 'form': form}

    return render(request, 'menus/create-menu.html', context)
    


def menuSelection(request):
    menus = Menus.objects.all()

    # get all puppies grams related to user
    puppies = Puppy.objects.filter(owner=request.user)
    puppies_grams = {}
    for puppy in puppies:
        puppies_grams[puppy.name] = { 'grams': puppy.grams, 'weight': puppy.weight, 'id': puppy.id }




    for menu in menus:
        menu.prices = {}
        nutrition_information = json.loads(menu.nutrition_information)
        menu.nutrition_information = nutrition_information
        percents = json.loads(menu.percents)

        ############# NO BORRAR, CONTIENE EL CODIGO PARA CALCULAR LOS GRAMOS POR CADA INGREDIENTE POR CADA MASCOTA QUE TENGA EL USUARIO! ############
        # for k, v in puppies_grams.items():
        #     menu.prices[k] = {}
        #     v = float(v)
        #     for percent_name, percent_value in percents.items():
        #         if '.' in percent_value:
        #             percent_value = float(percent_value)
        #         else:
        #             percent_value = int(percent_value)

        #         menu.prices[k][percent_name] = round((v * percent_value) / 100)

        for k, v in puppies_grams.items():
            grams = float(v.get('grams'))
            weight = float(v.get('weight'))
            menu.prices[k] = {'price': get_price_from_weight(grams, weight), 'grams': grams, 'id': v.get('id')}

    context = {'menus':menus, 'page': 'menu-selection'}
    return render(request, 'dishes/menu-selection.html', context)


def menuDetail(request, pk):
    menu = Menus.objects.get(id=pk)
    menu.percents = json.loads(menu.percents)
    menu.nutrition_information = json.loads(menu.nutrition_information)

    menu.prices = {}

    # get last puppy created
    puppy = Puppy.objects.filter(owner=request.user).last()
    puppies_grams = { 
        puppy.name: {
            'grams': float(puppy.grams),
            'price': get_price_from_weight(float(puppy.grams), float(puppy.weight)),
            'id' : puppy.id
        }
    }
    menu.prices = puppies_grams

    context = {'menu':menu, 'page': 'menu-detail'}
    return render(request, 'dishes/menu-selection.html', context)


def menuPet(request, pk):
    puppy = Puppy.objects.get(id=pk)

    if puppy.menu is None:
        return redirect('menu-selection')

    menu = Menus.objects.get(id=puppy.menu.id)
    menu.percents = json.loads(menu.percents)
    menu.nutrition_information = json.loads(menu.nutrition_information)

    menu.prices = {}
    puppies_grams = { 
        puppy.name: {
            'grams': float(puppy.grams),
            'price': get_price_from_weight(float(puppy.grams), float(puppy.weight)),
            'id' : puppy.id
        }
    }
    menu.prices = puppies_grams

    context = {'menu':menu, 'page': 'menu-pet', 'puppy': puppy}
    return render(request, 'dishes/menu-pet.html', context)