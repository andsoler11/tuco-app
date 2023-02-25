from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserCreateView.as_view(), name='user-create-api'),
    path('list/', views.UserListView.as_view(), name='user-list-api'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='user-detail-api'),
]