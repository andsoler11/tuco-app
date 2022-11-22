from django.urls import path
from . import views


urlpatterns = [
    path('', views.dishesHome, name="dishes"),
    path('menu/<str:pk>', views.menusHome, name="menus"),
    path('menu-pet/<str:pk>', views.menuPet, name="menu-pet"),
    path('edit-pet/<str:pk>', views.editPet, name="edit-pet"),
    path('menus/create', views.createMenu, name="menus-create"),
    path('menus/list', views.listMenus, name="menus-list"),
    path('menus/delete/<str:pk>', views.deleteMenu, name="menus-delete"),
    path('menus/update/<str:pk>', views.updateMenu, name="menus-update"),
    path('menu-selection/', views.menuSelection, name="menu-selection"),
    path('menu-detail/<str:pk>', views.menuDetail, name="menu-detail"),

]