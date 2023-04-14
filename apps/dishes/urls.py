from django.urls import path
from . import views


urlpatterns = [
    path('', views.formulate_home, name="dishes"),
    path('menu/<str:pk>', views.menus_home, name="menus"),
    path('menu/', views.menus_home, name="menus"),
    path('menu-pet/<str:pk>', views.menu_pet, name="menu-pet"),
    path('edit-pet/<str:pk>', views.edit_pet, name="edit-pet"),
    # path('menus/create', views.createMenu, name="menus-create"),
    # path('menus/list', views.listMenus, name="menus-list"),
    # path('menus/delete/<str:pk>', views.deleteMenu, name="menus-delete"),
    # path('menus/update/<str:pk>', views.updateMenu, name="menus-update"),
    path('menu-selection/', views.menu_selection, name="menu-selection"),
    path('menu-detail/<str:menu_id>/<str:pet_id>/', views.menu_detail, name='menu-detail'),
    path('menu-detail/<str:menu_id>/', views.menu_detail, name='menu-detail'),

]