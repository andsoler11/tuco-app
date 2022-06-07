from django.urls import path
from . import views


urlpatterns = [
    path('', views.dishesHome, name="dishes"),
    path('test', views.dishesTest, name="dishes2"),
]