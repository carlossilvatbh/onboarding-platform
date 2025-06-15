"""
URLs do app screening
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'screening'

router = DefaultRouter()
# router.register(r'example', views.ExampleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
