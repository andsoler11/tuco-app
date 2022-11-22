from django import forms
from django.forms import ModelForm
from .models import Puppy, Breeds, Menus

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


class MenusForm(ModelForm):
    class Meta:
        model = Menus
        fields = [
            'name', 
            'description', 
            'ingredients_description', 
            'nutrition_information', 
            'percents',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['ingredients_description'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['nutrition_information'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['percents'].widget.attrs.update({
            'class': 'form-control',
        })