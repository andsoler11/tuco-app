from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(max_length=500, blank=True, null=True)
    password = models.CharField(max_length=255, default='1234')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)
    

class CustomUser(AbstractUser):
    email_hash = models.CharField(max_length=255)
    email_mask = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    phone_number_mask = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    addresses = models.TextField(null=True, blank=True)


# class Cart(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
#     items = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.id)
    
#     def total_price(self):
#         return sum([item['price'] * item['quantity'] for item in self.items])
    