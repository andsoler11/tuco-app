from django.contrib.auth.decorators import login_required
import string
from unicodedata import name
from django.shortcuts import redirect, render
from .models import Breeds, Puppy
from .forms import PuppyForm
from .utils import *
import json
import os

YOUNG_AGE = 2
MIDDLE_AGE = 4
ADULT_AGE = 8


@login_required(login_url='login')
def dishesHome(request):
    page = 'multistep-form'
    form = PuppyForm()
    points = 0
    grams = 0
    grams_percent = 0
    dish = ''

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
        
        puppy = Puppy(
            owner=request.user, 
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

@login_required(login_url='login')
def menusHome(request, pk):
    page = 'menus'
    puppy_data = Puppy.objects.get(id=pk)

    grams = puppy_data.grams
    food = puppy_data.is_barf_active
    allergies = puppy_data.allergies
    special_needs = puppy_data.special_needs

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
    
    # get the price
    price = 7000 # this is by 500 grams
    price_grams = round((grams / 500) * price)
    
    context = {
        'page': page, 
        'grams': grams, 
        'puppy_data': puppy_data,
        'percent_ingredients': percent_ingredients, 
        'price_grams': price_grams,
        'allergies': allergies,
        'special_needs': special_needs
    }

    if food == 'no':
        context['week_percents'] = week_percents


    return render(request, 'dishes/menus.html', context)



