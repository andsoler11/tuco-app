# from unittest.mock import patch
# from django.test import TestCase
# from django.contrib.auth import get_user_model

# from apps.dishes import models

# def sample_user(email='test123@test.com', password='testpass'):
#     """create a sample user"""
#     return get_user_model().objects.create_user(email, password)

# class ModelTests(TestCase):

#     def test_create_puppy_with_name_successful(self):
#         name = 'test123'
#         puppy = models.Puppy.objects.create(
#             owner=sample_user(),
#             name=name
#         )

#         self.assertEqual(puppy.name, name)