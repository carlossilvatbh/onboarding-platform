#!/bin/bash

# Script para executar testes do projeto ONBOARDING

echo "🧪 Executando testes do projeto ONBOARDING..."

# Navegar para o diretório backend
cd backend

# Verificar se o ambiente virtual está ativo
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️ Ambiente virtual não detectado. Ativando..."
    source ../venv/bin/activate
fi

# Executar testes com diferentes configurações

echo "📋 1. Executando testes unitários..."
python -m pytest apps/ -v --tb=short -m "unit or models" --cov=apps --cov-report=term-missing

echo ""
echo "🌐 2. Executando testes de API..."
python -m pytest apps/ -v --tb=short -m "api or views" --cov=apps --cov-append

echo ""
echo "🔧 3. Executando testes de integração..."
python -m pytest apps/ -v --tb=short -m "integration" --cov=apps --cov-append

echo ""
echo "🚀 4. Executando todos os testes com coverage completo..."
python -m pytest apps/ -v --tb=short --cov=apps --cov-report=html --cov-report=term-missing --cov-fail-under=80

echo ""
echo "📊 5. Relatório de coverage gerado em htmlcov/index.html"

echo ""
echo "🔍 6. Executando verificações de qualidade de código..."

echo "   - Black (formatação)..."
black --check apps/ || echo "   ⚠️ Execute 'black apps/' para corrigir formatação"

echo "   - isort (imports)..."
isort --check-only apps/ || echo "   ⚠️ Execute 'isort apps/' para corrigir imports"

echo "   - flake8 (linting)..."
flake8 apps/ || echo "   ⚠️ Corrija os problemas de linting reportados"

echo ""
echo "✅ Testes concluídos!"

# Voltar ao diretório raiz
cd ..

