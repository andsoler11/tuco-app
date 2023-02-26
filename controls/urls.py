from django.urls import path
from . import views


urlpatterns = [
    path('breeds', views.renderBreeds, name="breeds"),
    path('breeds/<str:pk>', views.breedDetail, name="breed-detail"),
    path('email/send/button', views.sendEmailButton, name="send-email-button"),
]