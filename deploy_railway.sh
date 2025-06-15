#!/bin/bash

# Script de deploy para Railway.app
# CORREÇÃO: Automatiza deploy e resolve problemas identificados

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy para Railway.app..."

# Verificar se Railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI não encontrado. Instalando..."
    npm install -g @railway/cli
fi

# Verificar se está logado no Railway
if ! railway whoami &> /dev/null; then
    echo "🔐 Faça login no Railway:"
    railway login
fi

# Verificar se o projeto existe
if ! railway status &> /dev/null; then
    echo "📁 Criando novo projeto no Railway..."
    railway init
fi

echo "🔧 Configurando variáveis de ambiente..."

# Configurar variáveis de ambiente essenciais
railway variables set DJANGO_ENVIRONMENT=production
railway variables set PYTHONPATH=/app/backend
railway variables set PYTHONUNBUFFERED=1
railway variables set PYTHONDONTWRITEBYTECODE=1

# Configurar paths
railway variables set STATIC_ROOT=/app/backend/staticfiles
railway variables set MEDIA_ROOT=/app/backend/media

# Configurar segurança
railway variables set SECURE_SSL_REDIRECT=True
railway variables set SECURE_PROXY_SSL_HEADER="HTTP_X_FORWARDED_PROTO,https"

# Configurar Django
railway variables set ALLOWED_HOSTS="*.railway.app,localhost,127.0.0.1"
railway variables set CORS_ALLOWED_ORIGINS="https://*.railway.app"

echo "🗄️ Configurando banco de dados..."
# Adicionar PostgreSQL se não existir
if ! railway ps | grep -q postgres; then
    echo "Adicionando PostgreSQL..."
    railway add postgresql
fi

# Adicionar Redis se não existir
if ! railway ps | grep -q redis; then
    echo "Adicionando Redis..."
    railway add redis
fi

echo "🔑 Configurando SECRET_KEY..."
# Gerar SECRET_KEY se não existir
if ! railway variables | grep -q SECRET_KEY; then
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    railway variables set SECRET_KEY="$SECRET_KEY"
fi

echo "📦 Fazendo deploy..."
railway up --detach

echo "⏳ Aguardando deploy..."
sleep 30

echo "🏥 Verificando health check..."
RAILWAY_URL=$(railway domain)
if [ ! -z "$RAILWAY_URL" ]; then
    echo "Testando: https://$RAILWAY_URL/healthz"
    curl -f "https://$RAILWAY_URL/healthz" || echo "⚠️ Health check falhou"
else
    echo "⚠️ URL do Railway não encontrada"
fi

echo "📊 Status do deploy:"
railway status

echo "📝 Logs recentes:"
railway logs --tail 20

echo "✅ Deploy concluído!"
echo ""
echo "🌐 Acesse sua aplicação em: https://$RAILWAY_URL"
echo "🔧 Admin: https://$RAILWAY_URL/admin/"
echo "📚 API Docs: https://$RAILWAY_URL/api/docs/"
echo ""
echo "📋 Comandos úteis:"
echo "  railway logs           # Ver logs"
echo "  railway shell          # Acessar shell"
echo "  railway run python manage.py createsuperuser  # Criar superusuário"

