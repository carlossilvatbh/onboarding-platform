#!/bin/bash

# Script de setup para desenvolvimento local do projeto ONBOARDING

echo "🚀 Configurando projeto ONBOARDING para desenvolvimento..."

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

# Verificar versão do Python
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 Python version: $PYTHON_VERSION"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📚 Instalando dependências..."
cd backend
pip install -r requirements.txt

# Criar arquivo .env se não existir
if [ ! -f "../.env" ]; then
    echo "⚙️ Criando arquivo .env..."
    cp ../.env.example ../.env
    echo "✏️ Por favor, edite o arquivo .env com suas configurações locais"
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p staticfiles media logs

# Executar migrações
echo "🗄️ Executando migrações..."
python manage.py makemigrations
python manage.py migrate

# Coletar arquivos estáticos
echo "📄 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Criar superusuário (opcional)
echo "👤 Deseja criar um superusuário? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

echo "✅ Setup concluído!"
echo ""
echo "Para iniciar o servidor de desenvolvimento:"
echo "  cd backend"
echo "  python manage.py runserver"
echo ""
echo "Para executar os testes:"
echo "  cd backend"
echo "  python manage.py test"
echo ""
echo "Para usar Docker:"
echo "  docker-compose up -d"

