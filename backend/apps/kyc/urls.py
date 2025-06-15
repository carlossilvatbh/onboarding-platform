"""
URLs do app kyc
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'kyc'

router = DefaultRouter()
# router.register(r'example', views.ExampleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
