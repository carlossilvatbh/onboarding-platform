"""
Configuração do app risk
"""

from django.apps import AppConfig


class RiskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.risk'
    verbose_name = 'Risk'
