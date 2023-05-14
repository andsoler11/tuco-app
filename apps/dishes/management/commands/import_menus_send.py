import json
from django.core.management.base import BaseCommand
from apps.dishes.models import Menus, MenuSendData, Pet
from pprint import pprint
from utils.privacy import Privacy
from django.contrib.auth.models import Group, Permission
from apps.users.models import CustomUser


privacy = Privacy()

class Command(BaseCommand):
    help = 'Import menus send dta from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r') as file:
            menus_data = json.load(file)

        for menu in menus_data:
            menu_fields = menu['fields']
            menu_fields['pk'] = menu['pk']

            pet_id = menu_fields.pop('pet', None)
            if pet_id:
                pet = Pet.objects.get(pk=pet_id)
                menu_fields['pet'] = pet


            menu_id = menu_fields.pop('menu', None)
            if menu_id:
                menu = Menus.objects.get(pk=menu_id)
                menu_fields['menu'] = menu

            menu_insert = MenuSendData(**menu_fields)
            menu_insert.save()
