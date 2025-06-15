"""
Configuração do app screening
"""

from django.apps import AppConfig


class ScreeningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.screening'
    verbose_name = 'Screening'
