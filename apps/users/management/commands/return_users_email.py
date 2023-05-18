import json
from django.core.management.base import BaseCommand
from apps.users.models import CustomUser
from pprint import pprint
from utils.privacy import Privacy
from django.contrib.auth.models import Group, Permission


privacy = Privacy()

class Command(BaseCommand):
    help = 'Import users emails'

    def handle(self, *args, **options):
        users = CustomUser.objects.all()
        for user in users:
            print(user.email)
            email_decrypted = privacy.decrypt(user.email)
            print(email_decrypted)
