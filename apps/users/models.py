from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(max_length=500, blank=True, null=True)
    password = models.CharField(max_length=255, default='1234')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)