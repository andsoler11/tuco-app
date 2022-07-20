from django import forms
from django.forms import ModelForm
from .models import Puppy, Breeds

class PuppyForm(ModelForm):
    class Meta:
        model = Puppy
        fields = [
            'name', 
            'owner', 
            'age', 
            'breed',
            'body_image', 
            'reproductive_state', 
            'activity_level', 
            'weight', 
            'allergies',
            'special_needs',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['body_image'].widget.attrs.update({
            'class': 'form-control',
        })
