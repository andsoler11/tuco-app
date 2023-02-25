from rest_framework import serializers

from apps.dishes.models import Puppy

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puppy
        fields = '__all__'

