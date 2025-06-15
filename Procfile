# Procfile otimizado para Railway.app
# CORREÇÃO: Configuração otimizada para resolver problemas de deploy

# Web server com configurações otimizadas
web: cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --worker-class gthread --threads 2 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 50 --preload --access-logfile - --error-logfile -

# Worker Celery para processamento assíncrono
worker: cd backend && celery -A config worker --loglevel=info --concurrency=2 --max-tasks-per-child=1000

# Beat scheduler para tarefas periódicas
beat: cd backend && celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Comando de release para migrações e collectstatic
release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear

