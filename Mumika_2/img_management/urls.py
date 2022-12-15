from django.urls import include, path
from .views import test, get_images

urlpatterns = [
    path('testt/', test, name='test'),
    path('get_images', get_images, name='get_images'),
]