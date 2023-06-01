from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Breeds, Pet, ContactDetail, Menus, MenuSendData
from .forms import PetForm, MenusForm
from .utils import *
from utils.privacy import Privacy
from django.core.cache import cache
import json


privacy = Privacy()

YOUNG_AGE = 2
MIDDLE_AGE = 4
ADULT_AGE = 8

puppy_ages = {
    'small': 11,
    'medium': 12,
    'large': 18,
    'giant': 24
}


def formulate_home(request, menu_id=None):
    page = 'multistep-form'
    form = PetForm()
    points = 0
    grams = 0
    grams_percent = 0
    dish = ''
    user = None

    if request.method == 'POST':
        activity_level_input = request.POST.get('activity_level')
        reproductive_state_input = request.POST.get('reproductive_state')
        body_image_input = request.POST.get('body_image')

        age, age_type = validate_age_inputs(request.POST.get('age'), request.POST.get('age_type'))
        weight = format_weight(request.POST.get('weight'))

        # get the data!
        grams, grams_percent, points = determine_grams(
            activity_level=activity_level_input,
            reproductive_state=reproductive_state_input,
            body_image=body_image_input,
            weight=weight,
            age_type=age_type,
            age=age
        )

        if request.user.is_authenticated:
            owner = request.user
        else:
            owner = None
        ##########################################################

        ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR')
        if type(ip) == list:
            ip = ip[0]

        puppy = Pet(
            owner=owner,
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
            is_barf_active=request.POST.get('natural_food'),
            menu_id=menu_id,
            owner_ip_mask=Privacy.mask_ip(ip),
        )

        puppy.save()
        pk = puppy.id

        ################ section for user contact ################
        if request.POST.get('name_contact') and request.POST.get('email_contact'):
            email = request.POST.get('email_contact').lower()
            name = request.POST.get('name_contact').lower()

            if not '@' in email:
                return render(request, 'dishes/dishes-home.html',
                              {'page': page, 'form': form, 'error': 'El email no es valido'})

            contact = ContactDetail(
                name_contact=name,
                email_contact=privacy.secure_email(email)['encrypted'],
                pet=puppy
            )
            contact.save()
        ##########################################################

        if menu_id is not None:
            return redirect('list-pets')

        return redirect('menus', pk=pk)

    breeds = cache.get('breeds')
    if breeds is None:
        breeds = Breeds.objects.all().order_by('name')
        cache.set('breeds', breeds, 60 * 60 * 24)

    context = {
        'page': page,
        'dish': dish,
        'form': form,
        'grams': grams,
        'grams_percent': grams_percent,
        'points': points,
        'breeds': breeds
    }

    return render(request, 'dishes/home.html', context)


# @login_required(login_url='login')
def menus_home(request, pk=None):
    page = 'menus'
    available_menus = Menus.objects.all()
    puppy_data = None
    if pk is not None:
        puppy_data = Pet.objects.get(id=pk)
        for menu in available_menus:
            menu.price = get_price_from_weight(int(puppy_data.grams), float(puppy_data.weight))

    context = {
        'page': page,
        'pet': puppy_data,
        'available_menus': available_menus,
    }

    return render(request, 'dishes/menus.html', context)


def edit_pet(request, pk):
    puppy = Pet.objects.get(id=pk)
    form = PetForm(instance=puppy)

    if request.method == 'POST':
        menu = None
        if puppy.menu is not None:
            menu = puppy.menu.id

        puppy.delete()
        return formulate_home(request, menu)

    context = {'puppy': puppy, 'page': 'edit-pet', 'form': form}

    return render(request, 'dishes/edit-pet.html', context)


def create_menu(request):
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

    context = {'form': form, 'page': 'create-menu'}
    return render(request, 'menus/create-menu.html', context)


def list_menus(request):
    menus = Menus.objects.all()
    context = {'menus': menus, 'page': 'menus-list'}
    return render(request, 'menus/menus-list.html', context)


def delete_menu(request, pk):
    menu = Menus.objects.get(id=pk)

    if request.method == 'POST':
        # borramos de la BS y redireccionamos
        menu.delete()
        return redirect('menus-list')


def update_menu(request, pk):
    menu = Menus.objects.get(id=pk)

    if request.method == 'POST':
        menu.delete()
        return create_menu(request)

    menu.percents = convert_json_to_string(menu.percents)
    menu.nutrition_information = convert_json_to_string(menu.nutrition_information)

    form = MenusForm(instance=menu)
    context = {'menu': menu, 'page': 'update-menu', 'form': form}

    return render(request, 'menus/create-menu.html', context)


def menu_selection(request):
    menus = Menus.objects.all()

    # get all puppies grams related to user
    puppies = Pet.objects.filter(owner=request.user)
    puppies_grams = {}
    for puppy in puppies:
        puppies_grams[puppy.name] = {'grams': puppy.grams, 'weight': puppy.weight, 'id': puppy.id}

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

    context = {'menus': menus, 'page': 'menu-selection'}
    return render(request, 'dishes/menu-selection.html', context)


def menu_detail(request, menu_id, pet_id=None):
    menu = Menus.objects.get(id=menu_id)
    menu.percents = json.loads(menu.percents)
    menu.nutrition_information = json.loads(menu.nutrition_information)
    button_message = 'Agregar al carrito'
    puppy = None

    menu.prices = {}

    if pet_id:
        puppy = Pet.objects.get(id=pet_id)
        button_message = 'Agregar al carrito'
        puppies_grams = {
            puppy.name: {
                'grams': int(puppy.grams),
                'price': get_price_from_weight(float(puppy.grams), float(puppy.weight)),
                'id': puppy.id
            }
        }
        menu.prices = puppies_grams
    else:
        # get last puppy created
        if request.user.is_authenticated:
            puppy = Pet.objects.filter(owner=request.user).last()
            if puppy is None:
                return redirect('dishes')

        # puppies_grams = {
        #     puppy.name: {
        #         'grams': int(puppy.grams),
        #         'price': get_price_from_weight(float(puppy.grams), float(puppy.weight)),
        #         'id': puppy.id
        #     }
        # }
        # menu.prices = puppies_grams

    if request.method == 'POST':
        if pet_id:
            puppy.menu_id = menu.id
            puppy.save()

            menu_send_data = MenuSendData(
                menu=menu,
                pet=puppy,
                days_interval=15
            )
            menu_send_data.save()

            return redirect('list-pets')
        else:
            return redirect('menu-selection')

    context = {
        'menu': menu,
        'page': 'menu-detail',
        'button_message': button_message,
        'pet': puppy
    }

    return render(request, 'dishes/menu-selection.html', context)


def menu_pet(request, pk):
    puppy = Pet.objects.get(id=pk)

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
            'id': puppy.id
        }
    }
    menu.prices = puppies_grams

    context = {'menu': menu, 'page': 'menu-pet', 'puppy': puppy}
    return render(request, 'dishes/menu-pet.html', context)
