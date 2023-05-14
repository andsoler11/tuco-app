from django.contrib import admin
from apps.users.models import CustomUser
from django import forms

from utils.privacy import Privacy

privacy = Privacy()

class UsersAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.email:
            email = privacy.decrypt(self.instance.email)
            self.initial['email'] = email
        
        if self.instance and self.instance.phone_number:
            phone_number = privacy.decrypt(self.instance.phone_number)
            self.initial['phone_number'] = phone_number

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email_mask', 'phone_number_mask', 'last_login')
    form = UsersAdminForm