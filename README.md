# ONBOARDING - Digital KYC Platform

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.0+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/djangorestframework-3.15+-orange.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Plataforma digital de onboarding com funcionalidades de KYC (Know Your Customer), verificação OFAC/ONU/UE, OCR, dashboard em tempo real e suporte a internacionalização EN/PT.

## 🚀 Características

- **KYC Digital**: Processo completo de verificação de identidade
- **Screening**: Verificação contra listas OFAC, ONU e UE
- **OCR**: Processamento automático de documentos
- **Dashboard**: Monitoramento em tempo real
- **Multilíngue**: Suporte completo EN/PT-BR
- **API REST**: Arquitetura moderna com Django REST Framework
- **Celery**: Processamento assíncrono de tarefas
- **PostgreSQL**: Banco de dados robusto
- **Redis**: Cache e broker para Celery
- **Railway.app**: Deploy otimizado

## 🏗️ Arquitetura

```
ONBOARDING/
├── backend/                 # Django REST API
│   ├── apps/               # Aplicações Django
│   │   ├── core/          # Funcionalidades básicas
│   │   ├── users/         # Gestão de usuários
│   │   ├── kyc/           # Know Your Customer
│   │   ├── screening/     # Verificações OFAC/ONU/UE
│   │   ├── risk/          # Análise de risco
│   │   └── documents/     # Gestão de documentos
│   ├── config/            # Configurações Django
│   │   ├── settings/      # Settings por ambiente
│   │   ├── wsgi.py       # WSGI config
│   │   ├── asgi.py       # ASGI config
│   │   └── celery.py     # Celery config
│   └── manage.py          # Django management
├── frontend/              # React frontend (futuro)
├── docs/                  # Documentação
├── docker-compose.yml     # Docker para desenvolvimento
├── Procfile              # Railway.app config
├── nixpacks.toml         # Railway.app build config
└── requirements.txt      # Dependências Python
```

## 🛠️ Tecnologias

### Backend
- **Django 5.0 LTS**: Framework web Python
- **Django REST Framework 3.15**: API REST
- **Celery 5.4**: Processamento assíncrono
- **PostgreSQL**: Banco de dados principal
- **Redis**: Cache e message broker
- **Dynaconf**: Gerenciamento de configurações
- **Gunicorn**: Servidor WSGI para produção
- **WhiteNoise**: Servir arquivos estáticos

### Desenvolvimento
- **Docker**: Containerização
- **pytest**: Framework de testes
- **Black**: Formatação de código
- **isort**: Organização de imports
- **flake8**: Linting
- **mypy**: Type checking

### Deploy
- **Railway.app**: Plataforma de deploy
- **GitHub Actions**: CI/CD
- **Sentry**: Monitoramento de erros

## 🚀 Quick Start

### Pré-requisitos

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Git

### Instalação Local

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/onboarding.git
cd onboarding
```

2. **Execute o script de setup**
```bash
chmod +x setup.sh
./setup.sh
```

3. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Inicie o servidor**
```bash
cd backend
python manage.py runserver
```

### Usando Docker

1. **Inicie os serviços**
```bash
docker-compose up -d
```

2. **Execute as migrações**
```bash
docker-compose exec web python manage.py migrate
```

3. **Crie um superusuário**
```bash
docker-compose exec web python manage.py createsuperuser
```

## 🔧 Configuração

### Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```env
# Django
DJANGO_ENVIRONMENT=development
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_NAME=onboarding_dev
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis
CACHE_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

### Configurações por Ambiente

O projeto usa configurações separadas por ambiente:

- `config/settings/base.py`: Configurações comuns
- `config/settings/dev.py`: Desenvolvimento
- `config/settings/prod.py`: Produção

## 🧪 Testes

### Executar todos os testes
```bash
cd backend
python manage.py test
```

### Executar com coverage
```bash
pytest --cov=apps --cov-report=html
```

### Testes específicos
```bash
python manage.py test apps.users.tests
```

## 📊 Health Checks

O projeto inclui vários endpoints de monitoramento:

- `/healthz/`: Health check simples (200 OK)
- `/health/`: Health check detalhado (JSON)
- `/ready/`: Readiness check (migrations, etc.)
- `/alive/`: Liveness check

## 🚀 Deploy

### Railway.app

1. **Conecte seu repositório ao Railway**
2. **Configure as variáveis de ambiente**
3. **Deploy automático**

As configurações estão em:
- `Procfile`: Comandos de execução
- `nixpacks.toml`: Configuração de build

### Variáveis de Ambiente para Produção

```env
DJANGO_ENVIRONMENT=production
SECRET_KEY=your-production-secret
ALLOWED_HOSTS=your-domain.railway.app

# Database (Railway PostgreSQL)
PGDATABASE=railway_db
PGUSER=postgres
PGPASSWORD=railway_password
PGHOST=railway_host
PGPORT=5432

# Redis (Railway Redis)
CACHE_URL=redis://railway_redis_url
CELERY_BROKER_URL=redis://railway_redis_url
```

## 📚 API Documentation

A documentação da API está disponível em:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`
- OpenAPI Schema: `/api/schema/`

### Principais Endpoints

```
GET  /healthz/              # Health check
GET  /api/v1/auth/          # Autenticação
GET  /api/v1/kyc/           # KYC endpoints
GET  /api/v1/screening/     # Screening endpoints
GET  /api/v1/risk/          # Risk analysis
GET  /api/v1/documents/     # Document management
```

## 🔒 Segurança

### Configurações de Segurança

- HTTPS obrigatório em produção
- HSTS habilitado
- Cookies seguros
- CSRF protection
- XSS protection
- Content type sniffing protection
- Rate limiting configurado

### Autenticação

- Session-based authentication
- Token authentication
- Rate limiting por usuário/IP

## 🌍 Internacionalização

O projeto suporta múltiplos idiomas:

- **Inglês (en)**: Idioma padrão
- **Português Brasil (pt-br)**: Tradução completa

### Adicionar novas traduções

```bash
cd backend
python manage.py makemessages -l es  # Espanhol
python manage.py compilemessages
```

## 🔄 Celery Tasks

### Executar worker
```bash
cd backend
celery -A config worker --loglevel=info
```

### Executar beat scheduler
```bash
cd backend
celery -A config beat --loglevel=info
```

### Monitorar tasks
```bash
cd backend
celery -A config flower
```

## 📈 Monitoramento

### Logs

Os logs são configurados para diferentes níveis:
- **Development**: Console + arquivo
- **Production**: JSON estruturado

### Métricas

- Health checks automáticos
- Monitoramento de performance
- Alertas de erro via Sentry

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código

- Use `black` para formatação
- Use `isort` para imports
- Use `flake8` para linting
- Escreva testes para novas funcionalidades
- Mantenha coverage > 80%

## 📝 Changelog

### v1.0.0 (2025-06-15)
- ✅ Configuração inicial do projeto
- ✅ Django 5.0 LTS + DRF 3.15
- ✅ Celery 5.4 configurado
- ✅ Health checks implementados
- ✅ Configurações por ambiente
- ✅ Deploy Railway.app otimizado
- ✅ Estrutura de testes
- ✅ Documentação completa

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Documentação**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/onboarding/issues)
- **Email**: suporte@onboarding.com

## 👥 Equipe

- **Product Owner**: [Nome]
- **Head de Tecnologia**: [Nome]
- **Arquiteto de Software**: [Nome]
- **Especialistas**: Front-end, Back-end, QA, DevOps

---

**Desenvolvido com ❤️ pela equipe ONBOARDING**

