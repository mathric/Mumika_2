from django.urls import include, path
from .views import test_view

urlpatterns = [
    path('test/', test_view, name='main-view'),
]