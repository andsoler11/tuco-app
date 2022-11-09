from django.urls import path
from . import views


urlpatterns = [
    path('', views.dishesHome, name="dishes"),
    path('menus/<str:pk>', views.menusHome, name="menus"),
    path('edit-pet/<str:pk>', views.editPet, name="edit-pet"),

]