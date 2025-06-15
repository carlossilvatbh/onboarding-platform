#!/bin/bash

# Script para criar estrutura básica dos apps Django

APPS=("users" "kyc" "screening" "risk" "documents")
BASE_DIR="/home/ubuntu/onboarding_project/backend/apps"

for app in "${APPS[@]}"; do
    echo "Criando estrutura para app: $app"
    
    # Criar diretórios
    mkdir -p "$BASE_DIR/$app/migrations"
    mkdir -p "$BASE_DIR/$app/tests"
    
    # __init__.py
    echo "# App $app" > "$BASE_DIR/$app/__init__.py"
    echo "# Migrations para $app" > "$BASE_DIR/$app/migrations/__init__.py"
    echo "# Tests para $app" > "$BASE_DIR/$app/tests/__init__.py"
    
    # apps.py
    cat > "$BASE_DIR/$app/apps.py" << EOF
"""
Configuração do app $app
"""

from django.apps import AppConfig


class ${app^}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.$app'
    verbose_name = '${app^}'
EOF

    # models.py
    cat > "$BASE_DIR/$app/models.py" << EOF
"""
Models do app $app
"""

from django.db import models
from django.contrib.auth.models import User


# Adicione seus models aqui
EOF

    # views.py
    cat > "$BASE_DIR/$app/views.py" << EOF
"""
Views do app $app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render


# Adicione suas views aqui
EOF

    # urls.py
    cat > "$BASE_DIR/$app/urls.py" << EOF
"""
URLs do app $app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = '$app'

router = DefaultRouter()
# router.register(r'example', views.ExampleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
EOF

    # admin.py
    cat > "$BASE_DIR/$app/admin.py" << EOF
"""
Admin do app $app
"""

from django.contrib import admin
from . import models


# Registre seus models aqui
EOF

    # serializers.py
    cat > "$BASE_DIR/$app/serializers.py" << EOF
"""
Serializers do app $app
"""

from rest_framework import serializers
from . import models


# Adicione seus serializers aqui
EOF

    # tests/test_models.py
    cat > "$BASE_DIR/$app/tests/test_models.py" << EOF
"""
Testes para models do app $app
"""

from django.test import TestCase
from django.contrib.auth.models import User


class ${app^}ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_placeholder(self):
        """Teste placeholder"""
        self.assertTrue(True)
EOF

    # tests/test_views.py
    cat > "$BASE_DIR/$app/tests/test_views.py" << EOF
"""
Testes para views do app $app
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


class ${app^}ViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_placeholder(self):
        """Teste placeholder"""
        self.assertTrue(True)
EOF

done

echo "Estrutura dos apps criada com sucesso!"

