from django.urls import path, include
from .views import UploadFoodImage, UploadServiceImage


urlpatterns = [
    path('file/upload/food-image/', UploadFoodImage.as_view(), name='upload_food_image'),
    path('file/upload/service-image/', UploadServiceImage.as_view(), name='upload_service_image')
]