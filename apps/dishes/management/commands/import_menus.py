import json
from django.core.management.base import BaseCommand
from apps.dishes.models import Menus
from pprint import pprint
from utils.privacy import Privacy
from django.contrib.auth.models import Group, Permission
from apps.users.models import CustomUser


privacy = Privacy()

class Command(BaseCommand):
    help = 'Import menus from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r') as file:
            menus_data = json.load(file)

        for menu in menus_data:
            menu_fields = menu['fields']
            menu_fields['pk'] = menu['pk']

            menu_insert = Menus(**menu_fields)
            menu_insert.save()
