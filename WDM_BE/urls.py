from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('Authentication.urls')),
    path('', include('Lobby.urls')),
    path('', include('File.urls')),
    path('', include('Order.urls')),
    path('', include('Report.urls')),
    path('', include('FoodService.urls')),
    path('', include('User.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
