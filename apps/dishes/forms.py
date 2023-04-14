from django import forms
from django.forms import ModelForm
from .models import Pet, Menus
import json


class PetForm(ModelForm):
    class Meta:
        model = Pet
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


class MenusAdminForm(forms.ModelForm):
    class Meta:
        model = Menus
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            # Convert percents field from JSON to human-readable format
            if self.instance.percents:
                percents_dict = json.loads(self.instance.percents)
                percents_str = '\n'.join([f'{k}: {v}%' for k, v in percents_dict.items()])
                self.fields['percents'].initial = percents_str
            # Convert nutrition_information field from JSON to human-readable format
            if self.instance.nutrition_information:
                nutrition_dict = json.loads(self.instance.nutrition_information)
                nutrition_str = '\n'.join([f'{k}: {v}' for k, v in nutrition_dict.items()])
                self.fields['nutrition_information'].initial = nutrition_str
