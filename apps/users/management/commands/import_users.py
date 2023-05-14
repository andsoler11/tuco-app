import json
from django.core.management.base import BaseCommand
from apps.users.models import CustomUser
from pprint import pprint
from utils.privacy import Privacy
from django.contrib.auth.models import Group, Permission


privacy = Privacy()

class Command(BaseCommand):
    help = 'Import users from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r') as file:
            users_data = json.load(file)

        for user in users_data:
            user_data = user['fields']


            email_data = privacy.secure_email(user_data['email'])
            user_data['email_hash'] = email_data['hash']
            user_data['email_mask'] = email_data['mask']
            user_data['email'] = email_data['encrypted']
            user_data['username'] = email_data['mask']

            phone_data = privacy.encrypt('123456789')
            user_data['phone_number'] = phone_data
            user_data['phone_number_mask'] = Privacy.mask_phone_number('123456789')

            if user_data['last_name']:
                user_data['last_name'] = privacy.encrypt(user_data['last_name'])

            groups_data = user_data.pop('groups', [])
            user_permissions_data = user_data.pop('user_permissions', [])

            user_data['pk'] = user['pk']


            custom_user = CustomUser(**user_data)
            custom_user.save()

            # Assign groups to the custom_user using set() method
            custom_user.groups.set(Group.objects.filter(pk__in=groups_data))

            # Assign user_permissions to the custom_user using set() method
            custom_user.user_permissions.set(Permission.objects.filter(pk__in=user_permissions_data))
