# Guia de Deploy Railway.app - ONBOARDING

Este guia resolve os problemas de deploy identificados no relatório de pré-implementação.

## 🚀 Deploy Rápido

```bash
# 1. Executar script automatizado
chmod +x deploy_railway.sh
./deploy_railway.sh
```

## 📋 Deploy Manual

### 1. Pré-requisitos

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Fazer login
railway login
```

### 2. Configuração do Projeto

```bash
# Inicializar projeto
railway init

# Conectar repositório GitHub (opcional)
railway connect
```

### 3. Adicionar Serviços

```bash
# PostgreSQL
railway add postgresql

# Redis
railway add redis
```

### 4. Configurar Variáveis de Ambiente

#### Variáveis Essenciais

```bash
# Django
railway variables set DJANGO_ENVIRONMENT=production
railway variables set SECRET_KEY="your-secret-key-here"
railway variables set DEBUG=False

# Paths
railway variables set PYTHONPATH=/app/backend
railway variables set STATIC_ROOT=/app/backend/staticfiles
railway variables set MEDIA_ROOT=/app/backend/media

# Hosts permitidos
railway variables set ALLOWED_HOSTS="*.railway.app,localhost"
railway variables set CORS_ALLOWED_ORIGINS="https://*.railway.app"

# Segurança
railway variables set SECURE_SSL_REDIRECT=True
railway variables set SECURE_PROXY_SSL_HEADER="HTTP_X_FORWARDED_PROTO,https"
```

#### Variáveis de Banco (Automáticas)

O Railway configura automaticamente:
- `DATABASE_URL` (PostgreSQL)
- `REDIS_URL` (Redis)

### 5. Deploy

```bash
# Deploy
railway up

# Ou deploy com logs
railway up --detach
railway logs
```

## 🔧 Configurações Específicas

### Procfile

O projeto inclui um `Procfile` otimizado:

```
web: cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --worker-class gthread --threads 2 --timeout 120
worker: cd backend && celery -A config worker --loglevel=info --concurrency=2
beat: cd backend && celery -A config beat --loglevel=info
release: cd backend && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear
```

### nixpacks.toml

Configuração de build otimizada que resolve problemas de collectstatic:

- Instala dependências do sistema necessárias
- Configura Python 3.11
- Executa collectstatic com verbosidade
- Cria diretórios necessários

### railway.json

Configuração específica do Railway com:

- Health checks em `/healthz`
- Política de restart
- Configuração de volumes
- Timeout otimizado

## 🏥 Health Checks

O projeto inclui endpoints de monitoramento:

- `/healthz/` - Health check simples
- `/health/` - Health check detalhado
- `/ready/` - Readiness check
- `/alive/` - Liveness check

## 🐛 Resolução de Problemas

### Problema: Collectstatic falha

**Solução implementada:**
- Middleware personalizado para tratar erros
- Configuração otimizada no nixpacks.toml
- Criação de diretórios antes do collectstatic

### Problema: Timeout no deploy

**Solução implementada:**
- Timeout aumentado para 120s
- Workers otimizados (3 workers + threads)
- Health check timeout de 300s

### Problema: Variáveis de ambiente

**Solução implementada:**
- Script automatizado para configurar todas as variáveis
- Documentação clara de variáveis obrigatórias
- Validação de configuração

## 📊 Monitoramento

### Logs

```bash
# Ver logs em tempo real
railway logs

# Logs específicos
railway logs --service web
railway logs --service worker
```

### Status

```bash
# Status dos serviços
railway status

# Informações do projeto
railway info
```

### Métricas

Acesse o dashboard do Railway para:
- CPU e memória
- Requests por minuto
- Tempo de resposta
- Uptime

## 🔄 Comandos Úteis

### Gerenciamento

```bash
# Reiniciar serviço
railway restart

# Escalar workers
railway scale worker=2

# Acessar shell
railway shell
```

### Django

```bash
# Executar comandos Django
railway run python backend/manage.py createsuperuser
railway run python backend/manage.py migrate
railway run python backend/manage.py collectstatic

# Backup do banco
railway run python backend/manage.py dumpdata > backup.json
```

### Celery

```bash
# Monitorar tasks
railway run python backend/manage.py shell
>>> from celery import current_app
>>> current_app.control.inspect().active()
```

## 🔐 Segurança

### HTTPS

- Automático no Railway
- Certificados SSL gerenciados
- Redirecionamento HTTP → HTTPS configurado

### Variáveis Sensíveis

- SECRET_KEY gerada automaticamente
- Credenciais de banco automáticas
- Logs não expõem variáveis sensíveis

### Headers de Segurança

Configurados no middleware personalizado:
- HSTS
- CSP
- X-Frame-Options
- X-Content-Type-Options

## 📈 Performance

### Configurações Otimizadas

- Gunicorn com workers + threads
- Keep-alive configurado
- Max requests com jitter
- Preload da aplicação

### Cache

- Redis configurado para cache
- Sessions no Redis
- Cache de templates

### Static Files

- WhiteNoise para servir arquivos estáticos
- Compressão habilitada
- Cache headers otimizados

## 🆘 Suporte

### Problemas Comuns

1. **Build falha**: Verificar requirements.txt e nixpacks.toml
2. **App não inicia**: Verificar logs e variáveis de ambiente
3. **Database error**: Verificar se PostgreSQL foi adicionado
4. **Static files**: Verificar configuração STATIC_ROOT

### Contato

- Railway Support: https://railway.app/help
- Documentação: https://docs.railway.app
- Discord: https://discord.gg/railway

---

**Última atualização:** 15/06/2025
**Versão:** 1.0.0

