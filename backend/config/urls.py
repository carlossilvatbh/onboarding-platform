"""
Configuração de URLs principal do projeto ONBOARDING
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health checks e core
    path('', include('apps.core.urls')),
    
    # API endpoints
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/kyc/', include('apps.kyc.urls')),
    path('api/v1/screening/', include('apps.screening.urls')),
    path('api/v1/risk/', include('apps.risk.urls')),
    path('api/v1/documents/', include('apps.documents.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = "ONBOARDING Admin"
admin.site.site_title = "ONBOARDING Admin Portal"
admin.site.index_title = "Welcome to ONBOARDING Administration"

