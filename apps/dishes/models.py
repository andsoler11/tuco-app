from django.db import models
from django.contrib.auth.models import User
import uuid

BODY_IMAGES = {
    ('muy delgado', 'muy delgado'),
    ('delgado', 'delgado'),
    ('peso ideal', 'peso ideal'),
    ('sobrepeso', 'sobrepeso'),
}

REPRODUCTIVE_STATES = {
    ('castrado', 'castrado'),
    ('entero', 'entero'),
}

ALLERGIES_DATA = {
    ('Ninguna', 'Ninguna'),
    ('Pollo', 'Pollo'),
    ('Res', 'Res'),
    ('Cerdo', 'Cerdo'),
    ('Granos', 'Granos'),
    ('Huevo', 'Huevo'),
    ('Otro', 'Otro'),
    ('Pescado', 'Pescado'),
}

SPECIAL_NEEDS_DATA = {
    ('Ninguna', 'Ninguna'),
    ('Digestión', 'Digestión'),
    ('Piel', 'Piel'),
    ('Control de peso', 'Control de peso'),
    ('Cardiovascular', 'Cardiovascular'),
    ('Ariticulaciones', 'Ariticulaciones'),
    ('Urinario-renal', 'Urinario-renal'),
    ('Aliento', 'Aliento'),
    ('Ansiedad', 'Ansiedad'),
    ('Hiperactividad', 'Hiperactividad'),
    ('Cancer', 'Cancer'),
    ('Diabetes', 'Diabetes'),   
    ('Ganancia de peso', 'Ganancia de peso'),
}


class Puppy(models.Model):
    id                  = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner               = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name                = models.CharField(max_length=255)
    age                 = models.IntegerField(default=0)

    body_image          = models.CharField(max_length=255, null=False, blank=False, choices=BODY_IMAGES)
    reproductive_state  = models.CharField(max_length=255, null=False, blank=False, choices=REPRODUCTIVE_STATES)
    activity_level      = models.CharField(max_length=255, null=False, blank=False)

    allergies           = models.CharField(max_length=255, null=False, blank=False, choices=ALLERGIES_DATA, default='Ninguna')
    special_needs       = models.CharField(max_length=255, null=False, blank=False, choices=SPECIAL_NEEDS_DATA, default='Ninguna')

    breed               = models.CharField(max_length=255, null=True, blank=True)
    weight              = models.DecimalField(max_digits=12, decimal_places=6, default=0.0)
    grams               = models.DecimalField(max_digits=12, decimal_places=6, default=0.0)
    grams_percent       = models.DecimalField(max_digits=12, decimal_places=6, default=0.0)
    points              = models.IntegerField(default=0)
    is_barf_active      = models.CharField(max_length=255, null=True, blank=True)
    created             = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Breeds(models.Model):
    id          = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created     = models.DateTimeField(auto_now_add=True)
    name        = models.CharField(max_length=255)
    life_span   = models.CharField(max_length=255, null=True, blank=True)
    breed_group = models.CharField(max_length=255, null=True, blank=True)
    image_url   = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.name)
