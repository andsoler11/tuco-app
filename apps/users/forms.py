from django.contrib.auth.forms import UserCreationForm
from apps.users.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'phone_number', 'full_name']
