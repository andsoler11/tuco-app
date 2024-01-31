from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import PetSerializer, MenusSerializer
from apps.dishes.models import Pet, Menus
from utils.privacy import Privacy

privacy = Privacy()

class PetListView(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get(self, request, format=None):
        """function to get the pets of the user"""
        # return only the pets of the user
        pets = Pet.objects.filter(owner_id=request.user.id)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """function to create a new pet"""
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get(self, request, pk, format=None):
        """function to get the details of a pet"""
        pet = get_object_or_404(Pet, pk=pk)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """Function to update a pet"""
        pet_data = get_object_or_404(Pet, id=pk)
        serializer = PetSerializer(pet_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
  
        errors = serializer.errors
        error_messages = []
        for field, field_errors in errors.items():
            for error in field_errors:
                error_messages.append(f"{field}: {error}")
        return Response({"errors": error_messages}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """function to delete a pet"""
        pet = get_object_or_404(Pet, pk=pk)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PetCreateView(generics.CreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def post(self, request, format=None):
        """function to create a new pet"""
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenusView(generics.ListCreateAPIView):
    queryset = Menus.objects.all()
    serializer_class = MenusSerializer

    def get(self, request, format=None):
        """function to get all the menus"""
        # return only the pets of the user
        menus = Menus.objects.all()
        serializer = MenusSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """function to create a new menu"""

        required_fields = [
            'name', 
            'description',
            'percents',
        ]
        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MenusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        """function to update a menu"""
        menu = get_object_or_404(Menus, pk=pk)
        serializer = MenusSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """function to delete a menu"""
        menu = get_object_or_404(Menus, pk=pk)
        menu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminPetListView(generics.ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    def get(self, request, *args, **kwargs):
        """function to get all the pets"""

        # check if the user is superuser
        # if not request.user.is_superuser:
        #     return Response({'error': 'You are not authorized to access this resource'}, status=status.HTTP_401_UNAUTHORIZED)

        # return only the pets of the user
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

