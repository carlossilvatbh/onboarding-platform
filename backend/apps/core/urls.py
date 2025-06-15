"""
URLs do app core
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('healthz/', views.simple_health_check, name='health_check_simple'),
    path('health/', views.health_check, name='health_check_detailed'),
    path('ready/', views.readiness_check, name='readiness_check'),
    path('alive/', views.liveness_check, name='liveness_check'),
]

