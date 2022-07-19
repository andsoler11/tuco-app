from django.urls import path
from apps.users import views


urlpatterns = [
    path('', views.userLogin, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name='logout'),
]