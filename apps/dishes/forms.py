from django import forms
from django.forms import ModelForm
from .models import Puppy, GramsData

class PuppyForm(ModelForm):
    class Meta:
        model = Puppy
        fields = ['name', 'owner', 'age', 'body_image', 'reproductive_state', 'activity_level', 'weight']
