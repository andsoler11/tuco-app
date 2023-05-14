from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class PetApiTests(TestCase):
    """test the pets api"""

    def setUp(self):
        """setup the tests"""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='hola@hola.com',
            username='hola',
            password='testpass'
        )
        self.client.force_authenticate(self.user)   

        self.BASE_URL = reverse('pet-list-api')
        self.CREATE_URL = self.BASE_URL + 'create/'

        self.payload = {
            'owner': self.user.id,
            'name': 'test123',
            'breed': 'test123',
            'age': 8,
            'age_type': 'años',
            'body_image': 'sobrepeso',
            'reproductive_state': 'castrado',
            'activity_level': 'activo',
            'allergies': 'Ninguna',
            'special_needs': 'Ninguna',
            'breed': 'test',
            'weight': 1,
            'grams': 400,
            'grams_percent': 20,
            'points': 4,
            'is_barf_active': 'yes',
            'owner_ip_mask': '123.123.123.123'
        }

    def test_create_pet_successful(self):
        """test creating a new pet"""
        res = self.client.post(self.CREATE_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_pet_invalid(self):
        """test creating a new pet with invalid payload"""
        res = self.client.post(self.CREATE_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_all_pets(self):
        """test listing all pets"""
        # create a pet
        self.client.post(self.CREATE_URL, self.payload)
        # get the pets
        res = self.client.get(self.BASE_URL)
        # check the status code
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check the number of pets
        self.assertEqual(len(res.data), 1)
        # check the name of the pet
        self.assertEqual(res.data[0]['name'], self.payload['name'])

    def test_retrieve_pet(self):
        """test retrieving a pet"""
        # create a pet
        self.client.post(self.CREATE_URL, self.payload)
        # get the pet
        res = self.client.get(self.BASE_URL)
        # check the status code
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check the name of the pet
        self.assertEqual(res.data[0]['name'], self.payload['name'])

    def test_update_pet(self):
        """test updating a pet"""
        name_update = 'new name'

        # create a pet
        self.client.post(self.CREATE_URL, self.payload)
        # get the pet
        pets_response = self.client.get(self.BASE_URL)
        pet = pets_response.data[0]
        # update the pet
        pet['name'] = name_update

        # get the None values
        for key, value in pet.items():
            if value == None:
                pet[key] = ''

        res = self.client.put(self.BASE_URL + 'detail/' + pet['id'] + '/', pet)
        # check the status code
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check the name of the pet
        self.assertEqual(res.data['name'], name_update)

    def test_delete_pet(self):
        """test deleting a pet"""
        # create a pet
        self.client.post(self.CREATE_URL, self.payload)
        # get the pet
        pets_response = self.client.get(self.BASE_URL)
        pet = pets_response.data[0]
        # delete the pet
        res = self.client.delete(self.BASE_URL + 'detail/' + pet['id'] + '/')
        # check the status code
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # check the number of pets
        res = self.client.get(self.BASE_URL)
        self.assertEqual(len(res.data), 0)


class MenuApiTests(TestCase):
    """test the menu api"""

    def setUp(self):
        """setup the tests"""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='hola@hola.com',
            username='hola',
            password='testpass'
        )
        self.client.force_authenticate(self.user)

        self.BASE_URL = reverse('menus-api')

        self.payload = {
            'name': 'test123',
            'description': 'test123',
            'ingredients_description': 'test123',
            'nutrition_information': 'test123',
            'percents': 'test123',   
        }

    def test_create_menu_successful(self):
        """test creating a new menu"""
        res = self.client.post(self.BASE_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_menu_invalid(self):
        """test creating a new menu with invalid payload"""
        res = self.client.post(self.BASE_URL, {})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_all_menus(self):
        """test listing all menus"""
        # create a menu
        self.client.post(self.BASE_URL, self.payload)
        # get the menus
        res = self.client.get(self.BASE_URL)
        # check the status code
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # check the number of menus
        self.assertEqual(len(res.data), 1)
        # check the name of the menu
        self.assertEqual(res.data[0]['name'], self.payload['name'])
