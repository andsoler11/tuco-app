from django.urls import path
from . import views


urlpatterns = [
    path('', views.listPets, name="list-pets"),
    path('delete/<str:pk>', views.deletePet, name="delete-pet"),
    path('pet/menu/<str:pk>', views.editPetMenu, name="edit-pet-menu"),
]