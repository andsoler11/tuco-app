from django.db import models
import uuid

from django.forms import IntegerField

body_images = {
    (1, 'muy delgado'),
    (2, 'delgado'),
    (3, 'peso ideal'),
    (4, 'sobrepeso'),
    (5, 'obesidad'),
}

reproductive_states = {
    (1, 'castrado'),
    (2, 'entero'),
}

activity_levels = {
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
    # body_image = models.CharField(max_length=255, null=True, blank=True)
    body_image = models.IntegerField(null=False, blank=False, choices=body_images, default=3)

    # reproductive_state = models.CharField(max_length=255, null=True, blank=True)
    reproductive_state = models.IntegerField(null=False, blank=False, choices=reproductive_states, default=1)


    # activity_level = models.CharField(max_length=255, null=True, blank=True)
    activity_level = models.IntegerField(null=False, blank=False, choices=activity_levels, default=1)

    sex = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    points = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # options = models.ManyToManyField('MenuOption', blank=True)

    def __str__(self):
        return str(self.name)



class GramsData(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    ingrediente = models.CharField(max_length=255)
    diario = models.CharField(max_length=255)
    semanal = models.CharField(max_length=255)
    quincenal = models.CharField(max_length=255)
    mensual = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    puntos = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ingrediente)
