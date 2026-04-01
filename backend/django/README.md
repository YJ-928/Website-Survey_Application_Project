# Survey Application Platform – Backend

This repository contains the **Django backend** for the **Survey Application Platform (WE-POC)**.  
The system enables administrators to conduct structured surveys and view **aggregated, anonymized insights** through dashboards and charts — ensuring **privacy, data integrity, and scalability**.

This project is built as a **production‑ready Proof of Concept**, following clean architecture, secure authentication, controlled data collection, and strong logging practices.

---

## Prerequisites

- **Python** ≥ 3.11 (3.12 recommended)
- **pip** (bundled with Python) — or optionally **uv** / **Poetry** for dependency management
- **PostgreSQL** ≥ 14 (production) — SQLite is used by default in the POC

Verify your Python version:

```bash
python --version   # e.g. Python 3.12.3
pip --version      # e.g. pip 24.0
```

---

## Installation & Setup

### Option A — pip + venv (standard)

```bash
# Navigate to the backend directory
cd backend/django

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
# venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Option B — uv (fast Rust-based installer)

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

cd backend/django

# Create a virtual environment and install dependencies in one step
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Option C — Poetry

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

cd backend/django

# Install dependencies into an isolated environment
poetry install
poetry shell          # activate the environment
```

---

## Environment Variables

Copy the example below into a `.env` file inside `backend/django/`:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173

# Database (SQLite default — comment out for PostgreSQL)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=we_poc
# DB_USER=postgres
# DB_PASSWORD=your-db-password
# DB_HOST=localhost
# DB_PORT=5432

# JWT RSA Keys
JWT_PRIVATE_KEY_PATH=resource/jwt_signing_key.pem
JWT_PUBLIC_KEY_PATH=resource/jwt_verifying_key.pem

# RSA Encryption Keys
ENCRYPTION_PRIVATE_KEY_PATH=resource/enc_private_key.pem
ENCRYPTION_PUBLIC_KEY_PATH=resource/enc_public_key.pem

# JWT Lifetimes
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_MINUTES=7
JWT_ROTATE_REFRESH_TOKENS=True
JWT_REFRESH_BLACKLIST_AFTER_ROTATION=True

# Rate Limiting
ANON_RATE_LIMIT=50/minute
USER_RATE_LIMIT=100/minute

# Default Super Admin
DEFAULT_SUPER_ADMIN_EMAIL=admin@example.com
DEFAULT_SUPER_ADMIN_PASSWORD=ChangeMe123!
DEFAULT_SUPER_ADMIN_NAME=Super Admin
DEFAULT_SUPER_ADMIN_MOBILE=9000000000
DEFAULT_SUPER_ADMIN_LOCATION=Nalgonda

# Frontend
FRONTEND_BASE_URL=http://localhost:5173
FRONTEND_INVITE_PATH=/activate

# Email (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Seeding
SEED_DATA=True
```

---

## Database Migrations

```bash
# Apply all migrations (creates tables + seeds data if SEED_DATA=True)
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations
```

---

## Running the Development Server

```bash
python manage.py runserver
```

The API will be available at **http://127.0.0.1:8000**

### Useful endpoints

| URL | Purpose |
|-----|---------|
| `GET /health/` | Health check |
| `GET /api/docs/` | Swagger UI (interactive API docs) |
| `GET /api/redoc/` | ReDoc API docs |

---

## Objectives

- Conduct surveys while maintaining **respondent anonymity**
- Prevent free‑text misuse using **controlled dropdowns & enums**
- Provide **aggregated analytics** only (no PII leakage)
- Support **dynamic survey steps** driven from the database
- Enable **real email invitations** and admin onboarding
- Be **deployment‑ready** (Docker / PostgreSQL compatible)

---

## High‑Level System Flow

### Admin Flow
1. Default **Super Admin** is auto‑created post‑migration
2. Admin logs in using JWT (RSA‑based)
3. Admin invites other admins via email
4. Invitee activates account and sets password
5. Admin views dashboards & analytics

### Survey Flow
1. Survey schema (steps & questions) is fetched from backend
2. User submits survey answers (no auth required)
3. Backend validates answers against schema & enums
4. Responses are stored anonymously
5. Aggregated data powers dashboard charts

---

## Tech Stack

| Layer | Technology |
|-----|-----------|
Backend | Django 4.x, Django REST Framework |
Auth | JWT (RS256 – Public/Private keys) |
DB | SQLite (POC), PostgreSQL (Production) |
Email | Gmail SMTP (App Password) |
Docs | Swagger / OpenAPI (drf‑yasg) |
Logging | Python logging (file + console) |

---

## Poject Structure

```text
backend/
├── api/
│   ├── apps.py
│   ├── admin.py                  # Django admin configs
│   ├── urls.py                   # API routing
│   │
│   ├── models/
│   │   ├── admin.py              # Admin & invite models
│   │   ├── location.py           # District / Division / Mandal
│   │   ├── choice.py             # Choice categories & options
│   │   └── survey.py             # Survey schema & submissions
│   │
│   ├── serializers/
│   │   ├── admin.py
│   │   ├── location.py
│   │   ├── choice.py
│   │   ├── survey_schema.py
│   │   ├── survey_submission.py
│   │   └── dashboard.py
│   │
│   ├── views/
│   │   ├── admin.py
│   │   ├── location.py
│   │   ├── choices.py
│   │   ├── survey_schema.py
│   │   ├── survey_submit.py
│   │   └── dashboard.py
│   │
│   ├── services/
│   │   ├── email.py              # SMTP email logic
│   │   └── dashboard.py          # Aggregation helpers
│   │
│   ├── utils/
│   │   ├── default_admin.py      # Auto‑create super admin
│   │   ├── seed_locations.py     # Nalgonda district seed
│   │   └── seed_survey_data.py   # Survey schema seed
│
├── templates/
│   └── emails/
│       └── admin_invite.html
│
├── resource/
│   ├── jwt_signing_key.pem
│   └── jwt_verifying_key.pem
│
├── data/
│   └── survey_schema_v1.json
│
├── logs/
│   └── backend.log
│
├── .env
├── requirements.txt
├── manage.py
└── README.md
```

---

## Authentication & Security

- JWT Bearer Authentication
- Algorithm: **RS256**
- Public/Private keys loaded from `resource/`
- Passwords are **RSA‑encrypted** from frontend
- No plaintext passwords ever logged or stored

---

## Email Invitations

- Real email delivery via **Gmail SMTP**
- Secure invite links with expiry
- Email logic isolated in `api/services/email.py`
- Supports admin onboarding without manual DB access

---

## Location Master Data

- Hierarchy:
  - **District → Revenue Division → Mandal**
- Fully controlled (dropdown‑only)
- Seeded automatically for **Nalgonda District**
- Prevents invalid geographic data entry

---

## Survey Engine

### Dynamic Survey Schema
- Survey steps & questions are **DB‑driven**
- FE renders UI based on `/survey/schema/`
- Supports:
  - Conditional questions (`visible_when`)
  - Multiple input types (radio, checkbox)
  - Enum‑based validation

### Data Storage
- `SurveySubmission` → one response
- `SurveyAnswer` → per question answer
- No personal identifiers stored

---

## Dashboard & Analytics

All dashboard APIs are **authenticated** and **aggregated only**.

Available insights:
- Total & completed submissions
- Employment status distribution
- Age distribution
- Area type split
- Entrepreneur funnel
- Interests / Aspirations
- Submission mode
- District‑wise priority

Each chart has its **own endpoint**, making FE rendering simple and predictable.

---

## Logging & Error Handling

- Logs written to `logs/backend.log`
- Defensive `try/except` across:
  - Email sending
  - Survey submission
  - Dashboard aggregations
- **No sensitive data** logged (passwords, tokens, answers)

---

## Running the Project

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

### API Docs
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- Health Check: `GET /health/`

---

## Seeding Data

Enable in `.env`:
```env
SEED_DATA=True
```

Then run:
```bash
python manage.py migrate
```

Seeds:
- Default Super Admin
- Nalgonda District hierarchy
- Survey schema (steps, questions, choices)

---

## Status

✔ Survey submission  
✔ Dynamic schema  
✔ Aggregated dashboards  
✔ Email invitations  
✔ Production‑safe patterns  

---

## Notes

- FE & BE are **loosely coupled**
- Survey can evolve **without migrations**
- Ready for Docker & PostgreSQL

---

**Built for impact. Designed for privacy.**
