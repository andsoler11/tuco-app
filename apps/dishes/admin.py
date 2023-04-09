from django import forms
from .utils import convert_string_to_array, convert_json_to_string
import json

from django.contrib import admin
from .models import Menus, Breeds


class MenusAdminForm(forms.ModelForm):
    class Meta:
        model = Menus
        fields = '__all__'

    nutrition_information = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.nutrition_information:
            nutrition_str = convert_json_to_string(self.instance.nutrition_information)
            self.initial['nutrition_information'] = nutrition_str
        if self.instance and self.instance.percents:
            percents_str = convert_json_to_string(self.instance.percents)
            self.initial['percents'] = percents_str


@admin.register(Menus)
class MenusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_percents', 'get_nutrition_information')
    form = MenusAdminForm

    def get_percents(self, obj):
        percents_dict = json.loads(obj.percents)
        return ', '.join([f'{k}: {v}%' for k, v in percents_dict.items()])
    get_percents.short_description = 'Percents'

    def get_nutrition_information(self, obj):
        nutrition_dict = json.loads(obj.nutrition_information)
        print(nutrition_dict)
        return ', '.join([f'{k}: {v}' for k, v in nutrition_dict.items()])
    get_nutrition_information.short_description = 'Nutrition Information'

    def save_model(self, request, obj, form, change):
        if obj.nutrition_information:
            nutrition_dict = convert_string_to_array(obj.nutrition_information)
            obj.nutrition_information = json.dumps(nutrition_dict)

        if obj.percents:
            percents_dict = convert_string_to_array(obj.percents)
            obj.percents = json.dumps(percents_dict)
        super().save_model(request, obj, form, change)


@admin.register(Breeds)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed_size', 'life_span')
    search_fields = ('name',)