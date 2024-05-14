from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('Login.urls')),
    path('', include('Lobby.urls')),
    path('', include('Order.urls')),
    path('', include('Report.urls')),
    path('', include('FoodService.urls')),
    path('', include('User.urls')),
    path('admin/', admin.site.urls),
]
