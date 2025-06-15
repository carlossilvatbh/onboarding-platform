# BTS Global Bank - Digital KYC Platform

[![CI/CD Pipeline](https://github.com/carlossilvatbh/onboarding-platform/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/carlossilvatbh/onboarding-platform/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Django 5.0](https://img.shields.io/badge/django-5.0-green.svg)](https://www.djangoproject.com/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

> **be anywhere** - Secure, efficient, and compliant digital KYC platform for global banking solutions.

## 🏦 About BTS Global Bank

BTS Global Bank is a cutting-edge digital banking platform that provides comprehensive Know Your Customer (KYC) solutions for financial institutions worldwide. Our platform ensures regulatory compliance while delivering exceptional user experience.

## ✨ Features

### 🔐 Security & Compliance
- **Bank-grade security** with multi-layer encryption
- **Regulatory compliance** across multiple jurisdictions
- **Real-time fraud detection** with AI-powered algorithms
- **Secure document storage** with blockchain verification

### ⚡ Performance
- **Fast processing** - Reduce verification time from days to minutes
- **Scalable architecture** - Handle thousands of concurrent users
- **Real-time updates** - Instant status notifications
- **Mobile-optimized** - Seamless experience across all devices

### 🌍 Global Reach
- **Multi-language support** - English and Portuguese
- **Multi-currency** - Support for global transactions
- **International compliance** - GDPR, AML, KYC standards
- **24/7 availability** - Always accessible worldwide

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/carlossilvatbh/onboarding-platform.git
   cd onboarding-platform
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Servers**
   ```bash
   # Backend (Terminal 1)
   python manage.py runserver

   # Frontend (Terminal 2)
   cd frontend
   npm start
   ```

## 🏗️ Architecture

### Backend Stack
- **Django 5.0 LTS** - Web framework
- **Django REST Framework 3.15** - API development
- **PostgreSQL 15** - Primary database
- **Redis 7** - Caching and sessions
- **Celery 5.4** - Asynchronous task processing
- **JWT Authentication** - Secure token-based auth

### Frontend Stack
- **React 18** - User interface
- **Redux Toolkit** - State management
- **React Router 6** - Navigation
- **Axios** - HTTP client
- **Material-UI** - Component library

### Infrastructure
- **Railway.app** - Cloud deployment
- **GitHub Actions** - CI/CD pipeline
- **Docker** - Containerization
- **Nginx** - Reverse proxy

## 📋 KYC Process

### 1. Customer Registration
- Secure account creation
- Email verification
- Initial profile setup

### 2. Identity Verification
- Document upload (Passport, ID, Driver's License)
- Facial recognition verification
- Address verification

### 3. Risk Assessment
- **UBO Declaration** - Ultimate Beneficial Owner information
- **PEP Screening** - Politically Exposed Person checks
- **AML Compliance** - Anti-Money Laundering verification

### 4. Approval & Onboarding
- Automated risk scoring
- Manual review for high-risk cases
- Account activation and welcome

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/bts_onboarding
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Storage
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket

# External APIs
COMPLIANCE_API_KEY=your-compliance-api-key
DOCUMENT_VERIFICATION_API_KEY=your-verification-key
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### End-to-End Tests
```bash
npm run test:e2e
```

## 🚀 Deployment

### Railway.app Deployment

1. **Connect Repository**
   ```bash
   railway login
   railway link
   ```

2. **Set Environment Variables**
   ```bash
   railway variables set DATABASE_URL=postgresql://...
   railway variables set SECRET_KEY=...
   ```

3. **Deploy**
   ```bash
   railway up
   ```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t bts-onboarding .
docker run -p 8000:8000 bts-onboarding
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh JWT token

### KYC Endpoints
- `GET /api/kyc/profile/` - Get KYC profile
- `PUT /api/kyc/profile/` - Update KYC profile
- `POST /api/kyc/documents/` - Upload documents
- `GET /api/kyc/status/` - Get verification status

### UBO Endpoints
- `GET /api/ubo/declarations/` - List UBO declarations
- `POST /api/ubo/declarations/` - Create UBO declaration
- `PUT /api/ubo/declarations/{id}/` - Update UBO declaration

### PEP Endpoints
- `GET /api/pep/screening/` - Get PEP screening results
- `POST /api/pep/declaration/` - Submit PEP declaration

## 🔒 Security Features

- **HTTPS Enforcement** - All communications encrypted
- **CSRF Protection** - Cross-site request forgery prevention
- **XSS Protection** - Cross-site scripting prevention
- **Rate Limiting** - API abuse prevention
- **Input Validation** - Comprehensive data validation
- **Audit Logging** - Complete activity tracking

## 🌐 Internationalization

The platform supports multiple languages:
- **English (en)** - Primary language
- **Portuguese (pt-BR)** - Secondary language

### Adding New Languages

1. Create translation files:
   ```bash
   python manage.py makemessages -l es  # Spanish example
   ```

2. Translate strings in `locale/es/LC_MESSAGES/django.po`

3. Compile translations:
   ```bash
   python manage.py compilemessages
   ```

## 📊 Monitoring & Analytics

### Health Checks
- `GET /health/` - System health status
- `GET /health/db/` - Database connectivity
- `GET /health/redis/` - Redis connectivity

### Metrics
- User registration rates
- KYC completion rates
- Document verification success rates
- API response times

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write comprehensive tests
- Update documentation
- Follow semantic versioning

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [API Documentation](https://docs.btsglobalbank.com/api/)
- [User Guide](https://docs.btsglobalbank.com/user-guide/)
- [Developer Guide](https://docs.btsglobalbank.com/developers/)

### Contact
- **Email**: support@btsglobalbank.com
- **Phone**: +1 (555) 123-4567
- **Website**: [btsglobalbank.com](https://btsglobalbank.com)

### Community
- [GitHub Issues](https://github.com/carlossilvatbh/onboarding-platform/issues)
- [Discussions](https://github.com/carlossilvatbh/onboarding-platform/discussions)

## 🏆 Acknowledgments

- Django Software Foundation
- React Team
- Railway.app Team
- All contributors and supporters

---

**BTS Global Bank** - *be anywhere* 🌍

Made with ❤️ by the BTS Development Team

