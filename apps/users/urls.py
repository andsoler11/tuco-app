from django.urls import path
from apps.users import views


urlpatterns = [
    path('', views.renderHomepage, name="homepage"),
    path('login', views.userLogin, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('account/', views.account, name='account'),
    path('my-addresses/', views.myAddresses, name='addresses'),
    path('new-address/', views.newAddress, name='new-address'),
    path('recover-password/', views.recoverPassword, name='recover-password'),
    path('new-password-token/', views.newPasswordToken, name='new-password-token'),
    path('new-password/', views.newPassword, name='new-password'),
]