from django.urls import path
from . import views

urlpatterns = [
    path('', views.PetListView.as_view(), name='pet-list-api'),
    path('detail/<str:pk>/', views.PetDetailView.as_view(), name='pet-detail-api'),
    path('create/', views.PetCreateView.as_view(), name='pet-create-api'),
    path('menus/', views.MenusView.as_view(), name='menus-api'),
]