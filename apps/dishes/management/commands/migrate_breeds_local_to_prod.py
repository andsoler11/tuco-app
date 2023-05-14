import json
from django.core.management.base import BaseCommand
from apps.dishes.models import Menus, Breeds
from pprint import pprint
from utils.privacy import Privacy
from django.contrib.auth.models import Group, Permission
from apps.users.models import CustomUser


privacy = Privacy()

class Command(BaseCommand):
    help = 'Import breeds from local db to prod db'

    def handle(self, *args, **options):
        breeds = Breeds.objects.using('local').all()
        for breed in breeds:
            new_breed = Breeds(
                name=breed.name,
                life_span=breed.life_span,
                breed_group=breed.breed_group,
                image_url=breed.image_url,
            )
            new_breed.save()
