from pprint import pprint
from django.contrib.auth.decorators import login_required
import string
from unicodedata import name
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Breeds, Puppy, ContactDetail
from .forms import PuppyForm
from .utils import *
import json
import os

YOUNG_AGE = 2
MIDDLE_AGE = 4
ADULT_AGE = 8


# @login_required(login_url='login')
def dishesHome(request):
    page = 'multistep-form'
    form = PuppyForm()
    points = 0
    grams = 0
    grams_percent = 0
    dish = ''
    user = None 


    if request.method == 'POST':
        activity_level        = request.POST.get('activity_level')
        reproductive_state    = request.POST.get('reproductive_state')
        age_input             = request.POST.get('age')
        body_image            = request.POST.get('body_image')
        weight_input          = request.POST.get('weight')
        food_input            = request.POST.get('natural_food')
        weight, age           = format_weight_and_age(weight_input, age_input)
        
        # mind using sessions in the future
        # request.session['food_type'] = food_input
        grams, grams_percent, points = determineGrams(activity_level, reproductive_state, body_image, weight)


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
            
        puppy = Puppy(
            owner=user_upload, 
            name=request.POST.get('name'), 
            age=age_input,
            body_image=body_image,
            reproductive_state=reproductive_state,
            activity_level=activity_level,
            allergies=request.POST.get('allergies'),
            special_needs=request.POST.get('special_needs'),
            breed=request.POST.get('breed'),
            weight=weight,
            grams=grams,
            grams_percent=grams_percent,
            points=points,
            is_barf_active=food_input
        )
        puppy.save()
        pk = puppy.id

        if request.POST.get('name_contact') and request.POST.get('email_contact'):
            contact = ContactDetail(
                    name_contact=name,
                    email_contact=email,
                    pet=puppy
                )
            contact.save()

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
        'special_needs': special_needs
    }

    if food == 'no':
        context['week_percents'] = week_percents

    return render(request, 'dishes/menus.html', context)



