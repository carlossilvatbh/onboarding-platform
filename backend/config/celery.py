"""
Configuração do Celery para o projeto ONBOARDING
"""

import os
from celery import Celery

# Determina o ambiente baseado na variável DJANGO_ENVIRONMENT
environment = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if environment == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
elif environment == 'development':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

app = Celery('onboarding')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Configurações específicas do Celery
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Configurações de retry
app.conf.task_routes = {
    'apps.screening.*': {'queue': 'screening'},
    'apps.kyc.*': {'queue': 'kyc'},
    'apps.documents.*': {'queue': 'documents'},
}

@app.task(bind=True)
def debug_task(self):
    """Task de debug para testar o Celery"""
    print(f'Request: {self.request!r}')

