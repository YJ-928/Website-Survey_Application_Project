# Survey Application Platform – Backend

This repository contains the **Django backend** for the **Survey Application Platform (WE-POC)**.  
The system enables administrators to conduct structured surveys and view **aggregated, anonymized insights** through dashboards and charts — ensuring **privacy, data integrity, and scalability**.

This project is built as a **production‑ready Proof of Concept**, following clean architecture, secure authentication, controlled data collection, and strong logging practices.

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
