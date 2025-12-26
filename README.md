# MediSync SaaS

## 🎯 Overview

MediSync is an enterprise SaaS application that helps medical billing advocates generate professional, evidence-based insurance appeal letters automatically. Built with security-first architecture and HIPAA compliance at its core.

### Key Features

- 🔒 **HIPAA Secure**: Zero-retention architecture with encrypted processing
- 🧠 **AI-Powered**: Uses Groq's Llama 3.1 for intelligent appeal generation
- ⚡ **10x Faster**: Generate appeals in seconds instead of hours
- 📄 **OCR Processing**: Extract text from PDF denial letters automatically
- 💳 **SaaS-Ready**: Built-in authentication, subscriptions, and billing
- 🛡️ **Security-First**: Input sanitization, rate limiting, and comprehensive auditing

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Development](#-development)
- [Deployment](#-deployment)
- [Security](#-security)
- [Testing](#-testing)
- [Contributing](#-contributing)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Streamlit account
- API Keys: Groq, Supabase, Stripe
- Tesseract OCR (`apt-get install tesseract-ocr`)
- Poppler utilities (`apt-get install poppler-utils`)

### Local Development

```bash
# Clone the repository
git clone https://github.com/iabdullayev/medisync_saas.git
cd medisync_saas

# Install dependencies
pip install -r requirements.txt

# Configure secrets (copy template)
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your API keys

# Run the app
streamlit run app.py
```

Visit http://localhost:8501 to access the application.

---

## 🏗️ Architecture

### System Design

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────┐
│   Streamlit App (app.py)        │
│   - Authentication              │
│   - Rate Limiting               │
│   - Session Management          │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Processing Pipeline           │
│                                 │
│   1. OCR Engine                 │
│      └─ PDF → Text              │
│                                 │
│   2. LLM Engine                 │
│      ├─ Input Sanitization      │
│      └─ Groq API (Llama 3.1)   │
│                                 │
│   3. Output Formatting          │
│      └─ Appeal Letter           │
└─────────────────────────────────┘
```

### Zero-Retention Data Flow

```
Upload PDF → Temp File → OCR → Text (RAM) → LLM → Appeal (RAM) → Download → ∅
                ↓                                                              
         Immediate Delete
```

**No data is persisted:**
- PDFs are deleted immediately after OCR
- Text exists only in session memory
- Appeals are not stored server-side
- User downloads and saves locally

---

## 💻 Installation

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    tesseract-ocr \
    libgl1 \
    libglib2.0-0 \
    poppler-utils
```

**macOS:**
```bash
brew install tesseract poppler
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

**Core dependencies:**
- `streamlit==1.40.0` - Web framework
- `groq` - LLM API client
- `supabase` - Authentication backend
- `stripe` - Payment processing
- `pytesseract==0.3.10` - OCR engine
- `pdf2image==1.16.3` - PDF processing

---

## ⚙️ Configuration

### Environment Variables

Create `.streamlit/secrets.toml`:

```toml
# API Keys
GROQ_API_KEY = "gsk_..."
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "eyJhbGci..."
STRIPE_API_KEY = "sk_test_..."
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/..."
```

### Application Constants

Configuration is centralized in `src/constants.py`:

```python
# OCR Settings
OCR_DPI = 200  # Image quality for PDF conversion
MAX_PDF_PAGES = 50  # Maximum pages to process

# LLM Settings
LLM_MODEL = "llama-3.1-8b-instant"
MAX_CONTEXT_LENGTH = 6000  # Characters sent to LLM
LLM_TEMPERATURE = 0.1  # Low for consistency

# Security
MIN_PASSWORD_LENGTH = 8
RATE_LIMIT_REQUESTS = 5  # Per minute per user
```

### Project Structure

```
medisync-saas/
├── app.py                      # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── auth.py                 # Authentication & billing
│   ├── config.py               # Configuration management
│   ├── constants.py            # Application constants
│   ├── errors.py               # Custom exceptions
│   ├── llm_engine.py           # LLM integration
│   ├── ocr_engine.py           # PDF OCR processing
│   ├── pipeline.py             # Main processing pipeline
│   ├── rate_limiter.py         # Rate limiting
│   ├── sanitization.py         # Input sanitization
│   └── styles.py               # Shared CSS
├── .streamlit/
│   ├── config.toml             # Streamlit configuration
│   └── secrets.toml            # API keys (gitignored)
├── infra/                      # Infrastructure as Code
│   ├── main.tf                 # AWS resources
│   ├── variables.tf            # Terraform variables
│   └── outputs.tf              # Output values
├── requirements.txt            # Python dependencies
├── packages.txt                # System dependencies
└── README.md                   # This file
```

---

## 🔧 Development

### Running Locally

```bash
# Start the development server
streamlit run app.py

# With auto-reload
streamlit run app.py --server.runOnSave true
```

### Code Quality

```bash
# Run security audit
python security_audit.py .

# Format code
black src/ app.py

# Lint
pylint src/ app.py

# Type checking
mypy src/ app.py
```

### Adding Features

1. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Implement feature:**
   - Add code to appropriate module in `src/`
   - Update constants if needed
   - Add error handling
   - Add logging

3. **Test locally:**
   ```bash
   streamlit run app.py
   ```

4. **Run security audit:**
   ```bash
   python security_audit.py .
   ```

5. **Submit PR:**
   - Ensure all checks pass
   - Update documentation
   - Add tests

---

## 🚀 Deployment

### Streamlit Cloud

1. **Connect repository:**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Select your repository

2. **Configure secrets:**
   - Go to App Settings → Secrets
   - Paste contents of `.streamlit/secrets.toml`

3. **Deploy:**
   - Click "Deploy"
   - Monitor logs for errors

### AWS (Optional - API Backend)

```bash
cd infra/

# Create terraform.tfvars
cat > terraform.tfvars << EOF
groq_api_key = "gsk_..."
supabase_url = "https://..."
supabase_key = "eyJ..."
stripe_api_key = "sk_test_..."
EOF

# Deploy infrastructure
terraform init
terraform plan
terraform apply
```

**Resources created:**
- Lambda function for API
- API Gateway
- CloudFront distributions
- Route 53 DNS
- ACM certificates

---

## 🛡️ Security

### Security Features

✅ **Authentication**
- Supabase-based user authentication
- Email verification required
- Strong password requirements (8+ chars, number, special char)

✅ **Input Validation**
- Email regex validation
- Password strength checking
- LLM input sanitization (prompt injection prevention)
- File upload validation (type, size, signature)

✅ **Rate Limiting**
- 5 requests per minute per user
- Prevents API abuse and DoS attacks
- User-friendly error messages

✅ **Zero-Retention PHI Handling**
- No patient data stored in databases
- Temporary files deleted immediately
- Session-only memory storage
- HIPAA-compliant architecture

✅ **Secrets Management**
- All secrets in environment variables
- No hardcoded API keys
- `.gitignore` protection
- Terraform variable usage

### Security Audit

Run the automated security audit:

```bash
python security_audit.py .
```

**Expected output:**
```
✅ Passed:         20+
⚠️  Warnings:       ≤ 5
❌ Failed:         0
Critical Failures: 0

Estimated Failure Probability: < 0.05

🎉 RELEASE READY - All critical checks passed!
```

### Reporting Security Issues

**DO NOT** create public GitHub issues for security vulnerabilities.

Instead:
1. Email security@yourcompany.com
2. Include: Description, impact, steps to reproduce
3. Wait for acknowledgment (24 hours)
4. Coordinate disclosure timeline

---

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Test Structure

```python
# tests/test_auth.py
import pytest
from src.auth import validate_email, validate_password

def test_valid_email():
    assert validate_email("user@example.com") == True

def test_invalid_email():
    assert validate_email("not_an_email") == False

def test_strong_password():
    is_valid, msg = validate_password("Strong1!")
    assert is_valid == True
    assert msg == ""
```

### Test Coverage Goals

| Module | Target Coverage | Current |
|--------|----------------|---------|
| `auth.py` | 90%+ | TBD |
| `ocr_engine.py` | 80%+ | TBD |
| `llm_engine.py` | 70%+ | TBD |
| `pipeline.py` | 85%+ | TBD |

---

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes
4. Run tests: `pytest`
5. Run security audit: `python security_audit.py .`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open Pull Request

### Code Standards

- **Python**: Follow PEP 8
- **Docstrings**: Google style
- **Type hints**: Required for public functions
- **Tests**: Required for new features
- **Security**: Must pass audit

### Commit Messages

```
feat: Add rate limiting to appeal generation
fix: Resolve prompt injection vulnerability
docs: Update deployment instructions
test: Add tests for email validation
```

---

## 📄 License

**Proprietary Software**

Copyright © 2025 Your Company. All rights reserved.

This software is licensed for use only by authorized users.
Redistribution or modification is prohibited without written consent.

---

## 🙏 Acknowledgments

- [Groq](https://groq.com) - LLM API provider
- [Supabase](https://supabase.com) - Authentication backend
- [Stripe](https://stripe.com) - Payment processing
- [Streamlit](https://streamlit.io) - Application framework

---

## 📞 Support

- **Documentation**: docs.denialcopilot.com
- **Email**: support@denialcopilot.com
- **Security**: security@denialcopilot.com

---

## 🗺️ Roadmap

### v1.0 (Current)
- ✅ PDF upload and OCR
- ✅ AI appeal generation
- ✅ Authentication and billing
- ✅ Rate limiting
- ✅ Security audit

### v1.1 (Q1 2025)
- ⏳ Test coverage > 80%
- ⏳ Performance monitoring
- ⏳ Advanced analytics
- ⏳ Batch processing

### v2.0 (Q2 2025)
- 📋 Multiple LLM providers
- 📋 Custom templates
- 📋 Appeal tracking
- 📋 Integrations (EMR, PMS)

---

**Built with ❤️ for medical billing advocates**
