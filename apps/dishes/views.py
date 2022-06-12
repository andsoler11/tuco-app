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

# agregar campo de enfermedades

# file = os.path.abspath(os.path.dirname(__file__))

# with open(os.path.join(file, 'data.json')) as f:
#     BREEDS = json.load(f)
# BREEDS = json.load(json_data)


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
        activity_level = activity_mapping(activity_level_input)
        reproductive_state = reproductive_mapping(reproductive_state_input)

        
        if '.' in weight_input:
            weight = float(weight_input)
        else:
            weight = int(weight_input)

        if 'months' in age_input:
            age = int(age_input.split(' ')[0])
        else:
            age = int(age_input.split(' ')[0] * 12)


        size = 'large'
        if weight < 10:
            size = 'small'
        elif weight >= 10 and weight < 25:
            size = 'medium'
        elif weight >= 40:
            size = 'giant'


        puppy_ages = {
            'small': 11,
            'medium': 12,
            'large': 18,
            'giant': 24
        }

        grams_puppy_ages = {
            1: 100,
            2: 100,
            3: 90,
            4: 80,
            5: 70,
            6: 60,
            7: 60,
            8: 50,
            9: 50,
            10: 40,
            11: 40,
            12: 30
        }

        size_puppy_multiplier = {
            'small': 0.9,
            'medium': 1,
            'large': 1.5,
            'giant': 2
        }


        
        if age > puppy_ages[size]:
            grams, grams_percent, points = determineGrams(activity_level, reproductive_state, body_image, weight)
        else:
            grams_percent = grams_puppy_ages[age] / 10
            # grams = (grams_puppy_ages[age] * size_puppy_multiplier[size]) * weight
            grams = grams_puppy_ages[age] * weight

        return redirect('menus', str=grams)

        # dish = GramsData.objects.get(puntos=points)

    breeds = Breeds.objects.all()
    context = {'page': page, 'dish': dish, 'form': form, 'grams': grams, 'grams_percent': grams_percent, 'points': points, 'breeds':breeds}

    return render(request, 'dishes/home.html', context)



def menusHome(request, str):
    page = 'menus'
    grams = str

    context = {'page': page, 'grams': grams}
    return render(request, 'dishes/menus.html', context)