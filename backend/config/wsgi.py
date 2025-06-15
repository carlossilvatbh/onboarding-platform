"""
WSGI config for ONBOARDING project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Determina o ambiente baseado na variável DJANGO_ENVIRONMENT
environment = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if environment == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
elif environment == 'development':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_wsgi_application()

