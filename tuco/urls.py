from django.contrib import admin
from django.urls import path, include

api_version = 'v1.0'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('dishes/', include('apps.dishes.urls')),
    path('pets/', include('apps.pets.urls')),
    path('controls/', include('controls.urls')),
    path('api/' + api_version + '/users/', include('api.users_api.urls')),
    path('api/' + api_version + '/pets/', include('api.pets_api.urls')),
]
