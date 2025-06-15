"""
URLs do app risk
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'risk'

router = DefaultRouter()
# router.register(r'example', views.ExampleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
