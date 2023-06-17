from django.urls import path
from apps.users import views


urlpatterns = [
    path('', views.renderHomepage, name="homepage"),
    path('login', views.userLogin, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('account/', views.account, name='account'),
    path('addresses/', views.myAddresses, name='addresses'),
    path('new-address/', views.newAddress, name='new-address'),
    path('address-detail/', views.addressDetail, name='address-detail'),
    path('payment-methods/', views.paymentMethods, name='payment-methods'),
    path('new-method/', views.newPaymentMethod, name='new-method'),
    path('method-detail/', views.paymentMethodDetail, name='method-detail'),
    path('recover-password/', views.recoverPassword, name='recover-password'),
    path('new-password-token/', views.newPasswordToken, name='new-password-token'),
    path('new-password/', views.newPassword, name='new-password'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout')
]