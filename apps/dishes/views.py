import string
from unicodedata import name
from django.shortcuts import redirect, render
from .models import Breeds
from .forms import PuppyForm
from .utils import *
import json
import os

YOUNG_AGE = 2
MIDDLE_AGE = 4
ADULT_AGE = 8


def dishesHome(request):
    page = 'multistep-form'
    form = PuppyForm()
    points = 0
    grams = 0
    grams_percent = 0
    dish = ''

    if request.method == 'POST':
        activity_level_input = request.POST.get('activity_level')
        reproductive_state_input = request.POST.get('reproductive_state')
        age_input = request.POST.get('age')
        body_image = int(request.POST.get('body_image'))
        weight_input = request.POST.get('weight')
        food_input = request.POST.get('natural_food')
        activity_level = activity_mapping(activity_level_input)
        reproductive_state = reproductive_mapping(reproductive_state_input)
        weight, age = format_weight_and_age(weight_input, age_input)

        # mind using sessions in the future
        # request.session['food_type'] = food_input

        grams, grams_percent, points = determineGrams(activity_level, reproductive_state, body_image, weight)
    
        return redirect('menus', str=grams, food=food_input)

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



def menusHome(request, str, food):
    page = 'menus'
    grams = float(str)

    # mind using sessions in the future
    # food_type = request.session['food_type']

    # get the percents for each type of ingredient
    percent_ingredients = {}
    percent_ingredients['hueso carnoso'] = round((grams * 40) / 100)
    percent_ingredients['carnes'] = round((grams * 35) / 100)
    percent_ingredients['fruta/verdura'] = round((grams * 10) / 100)
    percent_ingredients['higado'] = round((grams * 5) / 100)
    percent_ingredients['visceras'] = round((grams * 10) / 100)
    grams = round(grams)


    if food == 'no':
        week_percents = {
            'Primera semana': {},
            'Segunda semana': {},
            'Tercera semana': {}
        }
        for k,v in percent_ingredients.items():
            week_percents['Primera semana'][k] = round(v/2)
            week_percents['Segunda semana'][k] = round(v/1.5)
            week_percents['Tercera semana'][k] = v



    # get the price
    price = 7000 # this is by 500 grams
    price_grams = round((grams / 500) * price)
    
    context = {
        'page': page, 
        'grams': grams, 
        'percent_ingredients': percent_ingredients, 
        'price_grams': price_grams,
    }

    if food == 'no':
        context['week_percents'] = week_percents


    return render(request, 'dishes/menus.html', context)