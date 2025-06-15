# Getting Started

Welcome to the ONBOARDING platform! This section will guide you through setting up and running the platform for the first time.

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.11+** - The platform is built with Python
- **Node.js 20+** - For frontend development and build tools
- **PostgreSQL 15+** - Primary database
- **Redis 7+** - Caching and message broker
- **Git** - Version control

### Optional but Recommended
- **Docker & Docker Compose** - For containerized development
- **Railway CLI** - For deployment to Railway.app
- **VS Code** - Recommended IDE with Python and Django extensions

## 🚀 Quick Start Options

Choose the setup method that best fits your needs:

### Option 1: Docker (Recommended)
Perfect for getting started quickly without installing dependencies locally.

```bash
# Clone the repository
git clone https://github.com/onboarding-team/onboarding.git
cd onboarding

# Start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:8000
```

### Option 2: Local Development
For active development and debugging.

```bash
# Clone the repository
git clone https://github.com/onboarding-team/onboarding.git
cd onboarding

# Run the setup script
chmod +x setup.sh
./setup.sh

# Activate virtual environment
source venv/bin/activate

# Start the development server
cd backend
python manage.py runserver
```

### Option 3: Railway.app Deployment
For production deployment.

```bash
# Clone the repository
git clone https://github.com/onboarding-team/onboarding.git
cd onboarding

# Deploy to Railway
chmod +x deploy_railway.sh
./deploy_railway.sh
```

## 🔧 Environment Configuration

The platform uses environment variables for configuration. Copy the example file and customize:

```bash
cp .env.example .env
```

### Essential Environment Variables

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
DJANGO_ENVIRONMENT=development

# Database
DB_NAME=onboarding
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Cache & Message Broker
CACHE_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0

# Security
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## 📊 Initial Setup

After starting the platform, you'll need to perform initial setup:

### 1. Database Migration
```bash
cd backend
python manage.py migrate
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

### 3. Load Sample Data (Optional)
```bash
python manage.py loaddata fixtures/sample_data.json
```

### 4. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

## 🌐 Accessing the Platform

Once everything is running, you can access:

| Service | URL | Description |
|---------|-----|-------------|
| **API** | http://localhost:8000/api/ | REST API endpoints |
| **Admin** | http://localhost:8000/admin/ | Django admin interface |
| **Docs** | http://localhost:8000/api/docs/ | Interactive API documentation |
| **Health** | http://localhost:8000/healthz/ | Health check endpoint |

## 🧪 Verify Installation

Run the verification script to ensure everything is working:

```bash
# Run health checks
python manage.py check --deploy

# Run tests
pytest

# Check translations
python manage.py check_translations
```

## 🔍 Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Verify connection
psql -h localhost -U postgres -d onboarding
```

#### Redis Connection Error
```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

#### Permission Denied
```bash
# Fix script permissions
chmod +x setup.sh
chmod +x deploy_railway.sh
chmod +x run_tests.sh
```

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](../deployment/troubleshooting.md)
2. Search [GitHub Issues](https://github.com/onboarding-team/onboarding/issues)
3. Create a new issue with detailed information

## 📚 Next Steps

Now that you have the platform running:

1. **Explore the API** - Visit the [API Documentation](../api/index.md)
2. **Understand the Architecture** - Read the [Architecture Overview](../architecture/index.md)
3. **Set up Development** - Follow the [Development Guide](../development/index.md)
4. **Deploy to Production** - Check the [Deployment Guide](../deployment/index.md)

---

**Need more detailed instructions?** Check out the specific guides:
- [Installation Guide](installation.md)
- [Configuration Guide](configuration.md)
- [First Steps Guide](first-steps.md)

