import json
from django.core.management.base import BaseCommand
from apps.dishes.models import Pet, Menus
from pprint import pprint
from utils.privacy import Privacy
from django.contrib.auth.models import Group, Permission
from apps.users.models import CustomUser


privacy = Privacy()

class Command(BaseCommand):
    help = 'Import pets from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r') as file:
            pets_data = json.load(file)

        for pet in pets_data:
            pet_fields = pet['fields']

            # if pet_fields['owner'] == 3:
            #     pet_fields['owner'] = 13

            # if pet_fields['owner'] == 2:    
            #     pet_fields['owner'] = 12

            # if pet_fields['owner'] == 8:
            #     pet_fields['owner'] = 14


            # Retrieve the owner instance from CustomUser model
            owner_id = pet_fields.pop('owner', None)
            if owner_id:
                owner = CustomUser.objects.get(pk=owner_id)
                pet_fields['owner'] = owner

            menu_id = pet_fields.pop('menu', None)
            if menu_id:
                menu = Menus.objects.get(pk=menu_id)
                pet_fields['menu'] = menu

            pet_fields['pk'] = pet['pk']


            pet_insert = Pet(**pet_fields)
            pet_insert.save()
