"""
Configurações do Django para o projeto ONBOARDING.
Seleciona automaticamente o ambiente baseado na variável DJANGO_SETTINGS_MODULE.
"""

import os

# Determina o ambiente baseado na variável de ambiente
environment = os.environ.get('DJANGO_ENVIRONMENT', 'dev')

if environment == 'production':
    from .prod import *
elif environment == 'development':
    from .dev import *
else:
    from .dev import *  # Default para desenvolvimento

