from django.urls import path
from . import views


urlpatterns = [
    path('', views.dishesHome, name="dishes"),
    path('menus/<str:str>/', views.menusHome, name="menus"),
]