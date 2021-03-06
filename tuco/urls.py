from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('dishes/', include('apps.dishes.urls')),
    path('pets/', include('apps.pets.urls')),
]
