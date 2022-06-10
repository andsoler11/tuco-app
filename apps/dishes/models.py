from django.db import models

import uuid

BODY_IMAGES = {
    (1, 'muy delgado'),
    (2, 'delgado'),
    (3, 'peso ideal'),
    (4, 'sobrepeso'),
    (5, 'obesidad'),
}

REPRODUCTIVE_STATES = {
    (1, 'castrado'),
    (2, 'entero'),
}

ACTIVITY_LEVELS = {
    (1, 'sedentario'),
    (2, 'actividad media'),
    (3, 'muy activo'),
}




class Puppy(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    age = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=255, null=True, blank=True)
    body_image = models.IntegerField(null=False, blank=False, choices=BODY_IMAGES, default=3)
    reproductive_state = models.IntegerField(null=False, blank=False, choices=REPRODUCTIVE_STATES, default=1)
    activity_level = models.IntegerField(null=False, blank=False, choices=ACTIVITY_LEVELS, default=1)
    breed = models.CharField(max_length=255, null=True, blank=True)
    sex = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    points = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Breeds(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    life_span = models.CharField(max_length=255, null=True, blank=True)
    breed_group = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.name)
