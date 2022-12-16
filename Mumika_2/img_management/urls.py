from django.urls import include, path
from .views import test, get_images, import_img_info_api, import_tags_api

urlpatterns = [
    path('testt/', test, name='test'),
    path('get_images', get_images, name='get_images'),
    path('import_img_info', import_img_info_api, name='import_img_info'),
    path('import_tag', import_tags_api, name='import_tag'),
]