"""
Middleware personalizado para o projeto ONBOARDING
Inclui correções para problemas identificados no relatório
"""

import logging
import time
from django.http import JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ValidationError
from django.db import connection
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class HealthCheckMiddleware(MiddlewareMixin):
    """
    Middleware para health checks
    Permite acesso aos endpoints de health sem autenticação
    """
    
    def process_request(self, request):
        """Processar requisição"""
        # Permitir health checks sem autenticação
        health_paths = ['/healthz/', '/health/', '/ready/', '/alive/']
        
        if request.path in health_paths:
            # Adicionar headers de cache para health checks
            request.META['HTTP_CACHE_CONTROL'] = 'no-cache'
        
        return None


class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Middleware para tratamento de erros
    CORREÇÃO: Trata erros de collectstatic e outros problemas do Railway
    """
    
    def process_exception(self, request, exception):
        """Processar exceções"""
        
        # Log do erro
        logger.error(f"Erro capturado pelo middleware: {str(exception)}", exc_info=True)
        
        # Tratar erros específicos do Railway/collectstatic
        if "collectstatic" in str(exception).lower():
            logger.warning("Erro de collectstatic detectado - possivelmente relacionado ao Railway")
            
            if settings.DEBUG:
                return JsonResponse({
                    'error': 'Static files collection error',
                    'message': 'This is likely a Railway deployment issue. Check STATIC_URL configuration.',
                    'debug_info': str(exception)
                }, status=500)
            else:
                return JsonResponse({
                    'error': 'Static files error',
                    'message': 'Please contact support if this persists.'
                }, status=500)
        
        # Tratar erros de validação UBO
        if "ubo" in str(exception).lower() and "nonetype" in str(exception).lower():
            logger.warning("Erro UBO NoneType detectado")
            return JsonResponse({
                'error': 'UBO validation error',
                'message': _('Error processing UBO declarations. Please ensure all required fields are filled.')
            }, status=400)
        
        # Tratar erros de banco de dados
        if "database" in str(exception).lower() or "connection" in str(exception).lower():
            logger.error("Erro de banco de dados detectado")
            return JsonResponse({
                'error': 'Database error',
                'message': _('Temporary database issue. Please try again in a moment.')
            }, status=503)
        
        # Para outros erros em produção, não expor detalhes
        if not settings.DEBUG:
            return JsonResponse({
                'error': 'Internal server error',
                'message': _('An unexpected error occurred. Please try again.')
            }, status=500)
        
        # Em desenvolvimento, deixar o Django tratar normalmente
        return None


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware para logging de requisições
    Útil para debugging e monitoramento
    """
    
    def process_request(self, request):
        """Iniciar timing da requisição"""
        request.start_time = time.time()
        
        # Log de requisições importantes
        if request.path.startswith('/api/'):
            logger.info(f"API Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}")
        
        return None
    
    def process_response(self, request, response):
        """Finalizar timing e log da resposta"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            # Log de requisições lentas
            if duration > 2.0:  # Mais de 2 segundos
                logger.warning(f"Slow request: {request.method} {request.path} took {duration:.2f}s")
            
            # Adicionar header de timing
            response['X-Response-Time'] = f"{duration:.3f}s"
        
        return response


class CORSMiddleware(MiddlewareMixin):
    """
    Middleware CORS personalizado
    CORREÇÃO: Configuração adequada de CORS para Railway.app
    """
    
    def process_response(self, request, response):
        """Adicionar headers CORS"""
        
        # Obter origem da requisição
        origin = request.META.get('HTTP_ORIGIN')
        
        # Origens permitidas
        allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
        
        # Em desenvolvimento, permitir localhost
        if settings.DEBUG:
            if origin and ('localhost' in origin or '127.0.0.1' in origin):
                response['Access-Control-Allow-Origin'] = origin
        else:
            # Em produção, verificar lista de origens permitidas
            if origin in allowed_origins:
                response['Access-Control-Allow-Origin'] = origin
        
        # Headers CORS padrão
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = (
            'Accept, Accept-Language, Content-Language, Content-Type, '
            'Authorization, X-Requested-With, X-CSRFToken'
        )
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Max-Age'] = '86400'  # 24 horas
        
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware para headers de segurança
    Adiciona headers de segurança não cobertos pelo Django
    """
    
    def process_response(self, request, response):
        """Adicionar headers de segurança"""
        
        # Content Security Policy
        if not settings.DEBUG:
            csp = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "font-src 'self' https:; "
                "connect-src 'self' https:; "
                "frame-ancestors 'none';"
            )
            response['Content-Security-Policy'] = csp
        
        # Outros headers de segurança
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Feature Policy (deprecated mas ainda usado por alguns browsers)
        response['Feature-Policy'] = 'geolocation "none"; microphone "none"; camera "none"'
        
        return response


class DatabaseHealthMiddleware(MiddlewareMixin):
    """
    Middleware para monitorar saúde do banco de dados
    """
    
    def process_request(self, request):
        """Verificar conexão com banco antes de processar requisição crítica"""
        
        # Verificar apenas para endpoints críticos
        critical_paths = ['/api/v1/kyc/', '/api/v1/screening/', '/admin/']
        
        if any(request.path.startswith(path) for path in critical_paths):
            try:
                # Teste simples de conexão
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
            except Exception as e:
                logger.error(f"Database connection failed: {str(e)}")
                return JsonResponse({
                    'error': 'Database unavailable',
                    'message': _('Service temporarily unavailable. Please try again.')
                }, status=503)
        
        return None

