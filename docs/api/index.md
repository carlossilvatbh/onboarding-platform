# API Documentation

The ONBOARDING platform provides a comprehensive REST API for managing KYC profiles, UBO declarations, PEP declarations, and documents. This section covers all available endpoints, authentication, and integration examples.

## 🔗 Base URL

```
Production: https://your-app.railway.app/api/v1/
Development: http://localhost:8000/api/v1/
```

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```http
Authorization: Bearer <your-jwt-token>
```

### Obtaining a Token

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
    "username": "your-username",
    "password": "your-password"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "username": "your-username",
        "email": "user@example.com"
    }
}
```

### Refreshing a Token

```http
POST /api/v1/auth/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 📊 Response Format

All API responses follow a consistent format:

### Success Response
```json
{
    "success": true,
    "data": {
        // Response data
    },
    "message": "Operation completed successfully"
}
```

### Error Response
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "field_name": ["This field is required"]
        }
    }
}
```

### Paginated Response
```json
{
    "success": true,
    "data": {
        "count": 100,
        "next": "http://api.example.com/accounts/?page=3",
        "previous": "http://api.example.com/accounts/?page=1",
        "results": [
            // Array of objects
        ]
    }
}
```

## 🏷️ Status Codes

| Code | Description |
|------|-------------|
| `200` | OK - Request successful |
| `201` | Created - Resource created successfully |
| `400` | Bad Request - Invalid request data |
| `401` | Unauthorized - Authentication required |
| `403` | Forbidden - Insufficient permissions |
| `404` | Not Found - Resource not found |
| `429` | Too Many Requests - Rate limit exceeded |
| `500` | Internal Server Error - Server error |

## 👤 KYC Profiles

### List KYC Profiles

```http
GET /api/v1/kyc/profiles/
Authorization: Bearer <token>
```

**Query Parameters:**
- `page` (int): Page number for pagination
- `page_size` (int): Number of items per page (max 100)
- `status` (string): Filter by status (`pending`, `in_review`, `approved`, `rejected`)
- `search` (string): Search by name or email

**Response:**
```json
{
    "success": true,
    "data": {
        "count": 25,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "full_name": "John Doe",
                "date_of_birth": "1990-01-15",
                "nationality": "Brazilian",
                "status": "pending",
                "annual_income": "50000.00",
                "created_at": "2025-06-15T10:30:00Z",
                "updated_at": "2025-06-15T10:30:00Z"
            }
        ]
    }
}
```

### Create KYC Profile

```http
POST /api/v1/kyc/profiles/
Authorization: Bearer <token>
Content-Type: application/json

{
    "full_name": "John Doe",
    "date_of_birth": "1990-01-15",
    "nationality": "Brazilian",
    "annual_income": "50000.00",
    "address_line1": "123 Main St",
    "city": "São Paulo",
    "state": "SP",
    "postal_code": "01234-567",
    "country": "Brazil"
}
```

### Get KYC Profile

```http
GET /api/v1/kyc/profiles/{id}/
Authorization: Bearer <token>
```

### Update KYC Profile

```http
PUT /api/v1/kyc/profiles/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "full_name": "John Doe Updated",
    "annual_income": "60000.00"
}
```

### Submit for Review

```http
POST /api/v1/kyc/profiles/{id}/submit-for-review/
Authorization: Bearer <token>
```

### Validation Status

```http
GET /api/v1/kyc/profiles/{id}/validation-status/
Authorization: Bearer <token>
```

**Response:**
```json
{
    "success": true,
    "data": {
        "profile_complete": true,
        "documents_complete": true,
        "ubo_validation": {
            "is_valid": true,
            "total_percentage": "100.00",
            "errors": []
        },
        "pep_validation": {
            "is_valid": true,
            "errors": []
        }
    }
}
```

## 🏢 UBO Declarations

### List UBO Declarations

```http
GET /api/v1/kyc/ubo-declarations/
Authorization: Bearer <token>
```

**Query Parameters:**
- `kyc_profile` (uuid): Filter by KYC profile ID
- `ownership_percentage__gte` (decimal): Minimum ownership percentage

### Create UBO Declaration

```http
POST /api/v1/kyc/ubo-declarations/
Authorization: Bearer <token>
Content-Type: application/json

{
    "kyc_profile": "123e4567-e89b-12d3-a456-426614174000",
    "full_name": "Jane Smith",
    "date_of_birth": "1985-03-20",
    "nationality": "American",
    "ownership_percentage": "25.50",
    "address_line1": "456 Oak Ave",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "United States"
}
```

### Validate UBO Ownership

```http
POST /api/v1/kyc/ubo-declarations/validate-ownership/
Authorization: Bearer <token>
Content-Type: application/json

{
    "kyc_profile": "123e4567-e89b-12d3-a456-426614174000"
}
```

## 🏛️ PEP Declarations

### List PEP Declarations

```http
GET /api/v1/kyc/pep-declarations/
Authorization: Bearer <token>
```

**Query Parameters:**
- `kyc_profile` (uuid): Filter by KYC profile ID
- `is_pep` (boolean): Filter by PEP status
- `pep_type` (string): Filter by PEP type
- `search` (string): Search in position or organization

### Create PEP Declaration

```http
POST /api/v1/kyc/pep-declarations/
Authorization: Bearer <token>
Content-Type: application/json

{
    "kyc_profile": "123e4567-e89b-12d3-a456-426614174000",
    "is_pep": true,
    "pep_type": "domestic",
    "position_held": "Minister of Finance",
    "organization": "Government of Brazil",
    "start_date": "2020-01-01",
    "end_date": "2024-12-31"
}
```

### PEP Summary

```http
GET /api/v1/kyc/pep-declarations/summary/
Authorization: Bearer <token>
```

**Response:**
```json
{
    "success": true,
    "data": {
        "total_declarations": 150,
        "pep_count": 25,
        "non_pep_count": 125,
        "by_type": {
            "domestic": 15,
            "foreign": 8,
            "international": 2
        }
    }
}
```

## 📄 Documents

### List Documents

```http
GET /api/v1/kyc/documents/
Authorization: Bearer <token>
```

**Query Parameters:**
- `kyc_profile` (uuid): Filter by KYC profile ID
- `document_type` (string): Filter by document type
- `ocr_processed` (boolean): Filter by OCR processing status

### Upload Document

```http
POST /api/v1/kyc/documents/
Authorization: Bearer <token>
Content-Type: multipart/form-data

{
    "kyc_profile": "123e4567-e89b-12d3-a456-426614174000",
    "document_type": "passport",
    "file": <binary-file-data>
}
```

### Process OCR

```http
POST /api/v1/kyc/documents/{id}/process-ocr/
Authorization: Bearer <token>
```

## 🔍 Search & Filtering

### Global Search

```http
GET /api/v1/search/
Authorization: Bearer <token>
?q=john&type=profile
```

**Query Parameters:**
- `q` (string): Search query
- `type` (string): Search type (`profile`, `ubo`, `pep`, `document`)

### Advanced Filtering

Most list endpoints support advanced filtering:

```http
GET /api/v1/kyc/profiles/
?status=approved
&created_at__gte=2025-01-01
&annual_income__gte=50000
&nationality=Brazilian
```

## 📊 Analytics

### Dashboard Stats

```http
GET /api/v1/analytics/dashboard/
Authorization: Bearer <token>
```

**Response:**
```json
{
    "success": true,
    "data": {
        "total_profiles": 1250,
        "pending_reviews": 45,
        "approved_profiles": 980,
        "rejected_profiles": 25,
        "completion_rate": 85.5,
        "avg_processing_time": "2.5 days"
    }
}
```

## 🚨 Error Handling

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `VALIDATION_ERROR` | Invalid input data | Check request format |
| `AUTHENTICATION_REQUIRED` | Missing or invalid token | Provide valid JWT token |
| `PERMISSION_DENIED` | Insufficient permissions | Check user roles |
| `RESOURCE_NOT_FOUND` | Resource doesn't exist | Verify resource ID |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Implement rate limiting |

### Error Response Example

```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid ownership percentage",
        "details": {
            "ownership_percentage": [
                "Total ownership percentage cannot exceed 100%"
            ]
        },
        "timestamp": "2025-06-15T10:30:00Z",
        "request_id": "req_123456789"
    }
}
```

## 🔄 Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Authenticated users**: 1000 requests per hour
- **Anonymous users**: 100 requests per hour

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## 📚 SDK & Examples

### Python SDK Example

```python
import requests

class OnboardingAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    
    def create_kyc_profile(self, data):
        response = requests.post(
            f'{self.base_url}/kyc/profiles/',
            json=data,
            headers=self.headers
        )
        return response.json()

# Usage
api = OnboardingAPI('https://your-app.railway.app/api/v1', 'your-token')
profile = api.create_kyc_profile({
    'full_name': 'John Doe',
    'date_of_birth': '1990-01-15',
    'nationality': 'Brazilian'
})
```

### JavaScript SDK Example

```javascript
class OnboardingAPI {
    constructor(baseUrl, token) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }
    
    async createKYCProfile(data) {
        const response = await fetch(`${this.baseUrl}/kyc/profiles/`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        });
        return response.json();
    }
}

// Usage
const api = new OnboardingAPI('https://your-app.railway.app/api/v1', 'your-token');
const profile = await api.createKYCProfile({
    full_name: 'John Doe',
    date_of_birth: '1990-01-15',
    nationality: 'Brazilian'
});
```

---

**Next**: Explore specific API sections:
- [Authentication Details](authentication.md)
- [KYC Profiles API](kyc-profiles.md)
- [UBO Declarations API](ubo-declarations.md)
- [PEP Declarations API](pep-declarations.md)
- [Documents API](documents.md)
- [Error Handling Guide](error-handling.md)

