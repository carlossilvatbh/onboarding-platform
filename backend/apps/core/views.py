"""
Views do app core, incluindo health check para Railway.app
"""

import json
import time
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import redis
from celery import current_app as celery_app


@require_http_methods(["GET"])
def health_check(request):
    """
    Health check endpoint para Railway.app e monitoramento.
    Retorna 200 OK se todos os serviços estão funcionando.
    """
    health_status = {
        'status': 'healthy',
        'timestamp': time.time(),
        'services': {}
    }
    
    overall_status = True
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['services']['database'] = 'healthy'
    except Exception as e:
        health_status['services']['database'] = f'unhealthy: {str(e)}'
        overall_status = False
    
    # Check cache (Redis)
    try:
        cache.set('health_check', 'ok', 30)
        if cache.get('health_check') == 'ok':
            health_status['services']['cache'] = 'healthy'
        else:
            health_status['services']['cache'] = 'unhealthy: cache test failed'
            overall_status = False
    except Exception as e:
        health_status['services']['cache'] = f'unhealthy: {str(e)}'
        overall_status = False
    
    # Check Celery (if configured)
    try:
        if hasattr(settings, 'CELERY_BROKER_URL'):
            # Simple check to see if Celery is configured
            inspect = celery_app.control.inspect()
            stats = inspect.stats()
            if stats:
                health_status['services']['celery'] = 'healthy'
            else:
                health_status['services']['celery'] = 'unhealthy: no workers'
                # Don't fail overall status for Celery in development
                if not settings.DEBUG:
                    overall_status = False
    except Exception as e:
        health_status['services']['celery'] = f'unhealthy: {str(e)}'
        if not settings.DEBUG:
            overall_status = False
    
    # Set overall status
    if not overall_status:
        health_status['status'] = 'unhealthy'
    
    # Return appropriate HTTP status
    status_code = 200 if overall_status else 503
    
    return JsonResponse(health_status, status=status_code)


@require_http_methods(["GET"])
def simple_health_check(request):
    """
    Health check simples que sempre retorna 200 OK.
    Usado pelo Railway.app para verificar se a aplicação está rodando.
    """
    return HttpResponse("OK", content_type="text/plain", status=200)


@require_http_methods(["GET"])
def readiness_check(request):
    """
    Readiness check para verificar se a aplicação está pronta para receber tráfego.
    """
    try:
        # Check if database migrations are up to date
        from django.core.management import execute_from_command_line
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connections
        
        executor = MigrationExecutor(connections['default'])
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            return JsonResponse({
                'status': 'not_ready',
                'reason': 'pending_migrations',
                'pending_migrations': len(plan)
            }, status=503)
        
        return JsonResponse({
            'status': 'ready',
            'timestamp': time.time()
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'status': 'not_ready',
            'reason': str(e)
        }, status=503)


@require_http_methods(["GET"])
def liveness_check(request):
    """
    Liveness check para verificar se a aplicação está viva.
    """
    return JsonResponse({
        'status': 'alive',
        'timestamp': time.time(),
        'version': getattr(settings, 'VERSION', '1.0.0')
    }, status=200)

