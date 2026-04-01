# Survey Application Platform

A full-stack survey platform built for the **Nalgonda district of Telangana, India** — collecting structured data from women across villages, mandals, and divisions, and surfacing aggregated insights through an analytics dashboard.

> Bilingual (English / Telugu) · Mobile-verified · Privacy-first · Production-ready

---

## Overview

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, TypeScript 5.9, Vite 7, Bootstrap 5, ECharts 6 |
| Backend | Django 4.2, Django REST Framework 3.14, SimpleJWT (RS256) |
| Database | PostgreSQL 16 (SQLite for local dev) |
| Deployment | Docker Compose, Nginx, Gunicorn |

---

## Features

- **Dynamic multi-step survey** — steps and questions served from the database, no frontend code change needed to evolve the survey
- **Mobile number verification** — unique submission per mobile, validated before form entry
- **Bilingual UI** — English and Telugu with a live language toggle
- **Conditional questions** — `visible_when` rules hide/show questions based on prior answers
- **Location hierarchy** — District → Revenue Division → Mandal → Village (cascading dropdowns, seeded for Nalgonda)
- **Admin dashboard** — JWT-protected analytics with 12+ chart types (ECharts)
- **Secure auth** — RS256 JWT, RSA-OAEP encrypted password transmission, email invite flow
- **Aggregated-only data** — no PII ever exposed through dashboard or analytics endpoints

---

## Repository Structure

```
├── backend/django/          # Django REST API
│   ├── api/                 # Models, serializers, views, services, utils
│   ├── backend/             # Django project settings
│   ├── data/                # Survey schema JSON
│   ├── resource/            # RSA key files
│   ├── templates/           # Email templates
│   └── logs/
│
├── frontend/                # React SPA
│   └── src/
│       ├── UI/Auth/         # Admin dashboard, invite, create-password
│       ├── UI/PreAuth/      # Public survey form, mobile verification
│       ├── services/        # API service layer
│       ├── context/         # FormContext, LanguageContext
│       ├── hooks/           # useProgressiveForm
│       └── shared/          # ECharts wrappers, reusable components
│
└── documents/               # DB schema, API docs, Postman collection
```

---

## Quick Start

### Prerequisites

| Tool | Minimum version |
|------|----------------|
| Python | 3.11 (3.12 recommended) |
| Node.js | 18 LTS (20 or 22 recommended) |
| npm | 9.x |
| PostgreSQL | 14+ (optional — SQLite used by default) |

---

### 1 · Clone the repository

```bash
git clone https://github.com/your-username/Website-Survey_Application_Project.git
cd Website-Survey_Application_Project
```

---

### 2 · Backend setup

```bash
cd backend/django

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
# venv\Scripts\activate           # Windows

# Install Python dependencies
pip install -r requirements.txt

# Copy and fill in environment variables
cp .env.example .env              # edit .env with your settings

# Run database migrations (seeds data if SEED_DATA=True in .env)
python manage.py migrate

# Start the development server
python manage.py runserver
```

Backend available at: **http://127.0.0.1:8000**  
Swagger docs at: **http://127.0.0.1:8000/api/docs/**

---

### 3 · Frontend setup

```bash
# From the project root
cd frontend

# Install Node.js dependencies
npm install

# Copy and fill in environment variables
cp .env.example .env              # set VITE_API_BASE_URL=http://localhost:8000

# Start the Vite development server
npm run dev
```

Frontend available at: **http://localhost:5173**

---

### 4 · Docker Compose (full stack)

```bash
# From the project root
docker compose up --build
```

| Service | URL |
|---------|-----|
| Frontend (Nginx) | http://localhost |
| Backend (Gunicorn) | http://localhost:8000 |
| API docs | http://localhost:8000/api/docs/ |

---

## Environment Variables — Quick Reference

### Backend (`backend/django/.env`)

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
JWT_PRIVATE_KEY_PATH=resource/jwt_signing_key.pem
JWT_PUBLIC_KEY_PATH=resource/jwt_verifying_key.pem
ENCRYPTION_PRIVATE_KEY_PATH=resource/enc_private_key.pem
ENCRYPTION_PUBLIC_KEY_PATH=resource/enc_public_key.pem
DEFAULT_SUPER_ADMIN_EMAIL=admin@example.com
DEFAULT_SUPER_ADMIN_PASSWORD=ChangeMe123!
SEED_DATA=True
```

### Frontend (`frontend/.env`)

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## API Highlights

| Category | Example endpoint |
|----------|-----------------|
| Auth | `POST /api/auth/admin/login/` |
| Survey | `GET /api/survey/schema/` · `POST /api/survey/submit/` |
| Locations | `GET /api/locations/villages/?mandal_id=1` |
| Dashboard | `GET /api/dashboard/summary/` |
| Analytics | `GET /api/analytics/question/{id}/` |

All list endpoints accept `?lang=te` for Telugu responses.  
Full interactive documentation: **`/api/docs/`**

---

## Documentation

| File | Contents |
|------|---------|
| [backend/django/README.md](backend/django/README.md) | Backend setup, env vars, migrations, project structure |
| [frontend/README.md](frontend/README.md) | Frontend setup, scripts, pages, component guide |
| [documents/README.md](documents/README.md) | DB schema, Postman collection, API design notes |

---

## License

This project is built as a proof-of-concept for social impact. See [LICENSE](LICENSE) for details.

---

**Built for impact. Designed for privacy.**
