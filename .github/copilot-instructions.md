# Copilot Instructions — Survey Application

## Architecture Overview

This is a **Survey Application** for the Nalgonda district of Telangana, India. It collects survey data from women across villages, mandals, and divisions, then provides analytics dashboards to administrators.

### System Architecture

```
┌─────────────────────┐       ┌──────────────────────┐       ┌────────────────┐
│  React 19 + TS      │ REST  │  Django 4.2 + DRF    │       │  PostgreSQL 16 │
│  (Vite, Bootstrap 5)│──────▶│  (JWT RS256, RSA-OAEP)│──────▶│  (Docker)      │
│  Port 5173          │       │  Port 8000            │       │  Port 5432     │
└─────────────────────┘       └──────────────────────┘       └────────────────┘
```

- **Frontend**: React 19, TypeScript, Vite 7, Bootstrap 5 + React Bootstrap, ECharts 6
- **Backend**: Django 4.2, Django REST Framework, SimpleJWT (RS256), drf-yasg (Swagger)
- **Database**: PostgreSQL 16 with location hierarchy and survey schema
- **Deployment**: Docker Compose with Nginx reverse proxy, Gunicorn WSGI server

### Monorepo Structure

```
├── backend/django/      # Django REST API
│   ├── api/             # Main app (models, views, serializers, services, utils)
│   └── backend/         # Django project settings
├── frontend/            # React SPA
│   └── src/
│       ├── UI/Auth/     # Admin dashboard, invite, create-password
│       ├── UI/PreAuth/  # Public survey form, mobile verification
│       ├── services/    # API service layer
│       ├── context/     # React Context (Form, Language)
│       ├── hooks/       # useProgressiveForm
│       └── shared/      # Charts (ECharts), form fields, navbar
└── documents/           # DB schema, API docs, data files
```

### Domain Entities

| Entity | Purpose |
|--------|---------|
| District → RevenueDivision → Mandal → Village | 4-level location hierarchy (Nalgonda) |
| SurveyStep → SurveyQuestion | Dynamic survey schema loaded from JSON |
| ChoiceCategory → ChoiceOption | Reusable option sets for questions |
| SurveySubmission → SurveyAnswer | One submission per mobile number, multiple answers |
| Admin / AdminInvite | Admin user management with email invite flow |

---

## Repository Coding Standards

### General

- Use **English** for all code, comments, and commit messages.
- Follow the existing file/folder naming conventions in each sub-project.
- Never hardcode secrets, API keys, or credentials. Use environment variables.
- All new features must maintain support for **English and Telugu** languages.

### Python / Django

- **Python 3.11+**, Django 4.2.x, DRF 3.14+
- Follow PEP 8. Use `snake_case` for functions, variables, and file names.
- Models go in `api/models/` — one file per domain (e.g., `survey.py`, `location.py`).
- Serializers go in `api/serializers/` — grouped by concern (e.g., `survey_schema.py`, `survey_submission.py`).
- Views go in `api/views/` — one file per feature area (e.g., `dashboard.py`, `analytics.py`).
- Services go in `api/services/` for business logic that doesn't belong in views.
- Utils go in `api/utils/` for standalone helpers (encryption, seeding, translations).
- Always register new model modules in `api/models/__init__.py`.
- Views and serializers are imported directly by path in `api/urls.py` — their `__init__.py` files are intentionally empty.
- Use `select_related` / `prefetch_related` for query optimization — never allow N+1 queries.
- Use `transaction.atomic()` for multi-model write operations.
- Use `bulk_create()` for batch inserts.

### TypeScript / React

- **React 19**, TypeScript 5.9, strict mode enabled.
- Use functional components with hooks. No class components.
- File naming: PascalCase for components (e.g., `SurveyForm.tsx`), camelCase for services/hooks.
- State management: React Context API only (FormContext, LanguageContext). No Redux.
- API calls go in `src/services/` — one service per backend domain.
- Reusable UI goes in `src/shared/components/` and `src/shared/charts/`.
- Page components: `src/UI/Auth/` (protected) and `src/UI/PreAuth/` (public).
- Custom hooks in `src/hooks/`.
- Translations in `src/constants/translations.ts` — use the `t(key, language)` function.
- Use Bootstrap 5 classes and React Bootstrap components for layout and styling.
- All chart components use ECharts and accept `{ name: string; value: number }[]` data prop.

---

## Backend Development Rules

### Models

- Every model must have a `__str__` method.
- Use `PROTECT` on delete for `SurveySubmission` → location ForeignKeys (prevent accidental deletion of referenced locations).
- Use `CASCADE` on delete within the location hierarchy (RevenueDivision→District, Mandal→Division, Village→Mandal).
- Use `CASCADE` on delete for answers when their parent submission is deleted.
- Use `SET_NULL` on delete for `SurveyQuestion.options_category` → `ChoiceCategory` (category removal shouldn't delete questions).
- UUID primary keys for submissions (`submission_id`).
- Add database indexes on frequently queried fields (e.g., `mobile_number`, `created_at`, `reference_id`).
- JSONField for flexible data: `SurveyAnswer.value`, `SurveyQuestion.visible_when`.

### Serializers

- Separate read and write serializers when input/output shapes differ.
- Pass `language` through serializer context for i18n: `self.context.get('language', 'en')`.
- Validate at the serializer level, not in views. Keep views thin.
- For survey submission: validate location hierarchy depth, required fields with `visible_when` logic, and option whitelisting.

### Views

- Use DRF `APIView` for custom logic; `generics` for simple CRUD.
- Set explicit `permission_classes`: `AllowAny` for public endpoints, `IsAuthenticated` for admin.
- Always pass `language` from query param to serializer context:
  ```python
  language = request.query_params.get('lang', 'en')
  serializer = MySerializer(data, context={'language': language})
  ```
- Return proper HTTP status codes: 200 (success), 201 (created), 400 (validation error), 401 (unauthorized), 404 (not found).

### Authentication

- JWT with **RS256** algorithm (asymmetric keys). Never use HS256.
- Passwords encrypted client-side with **RSA-OAEP** public key, decrypted server-side with private key.
- Access token: 60 minutes. Refresh token: 7 minutes. Rotate on refresh.
- Admin invite flow: invite → email link → activate with password → JWT login.

### Database Migrations

- Always create migrations for model changes: `python manage.py makemigrations`.
- Seed data runs via post-migrate signals controlled by `SEED_DATA` env flag.
- Never modify existing migrations. Create new ones.

---

## Frontend Development Rules

### Component Guidelines

- Every page component lives under `src/UI/Auth/` (requires login) or `src/UI/PreAuth/` (public).
- Shared/reusable components under `src/shared/components/`.
- Chart components under `src/shared/charts/` — all follow the ECharts pattern.
- Use `ProtectedRoute` wrapper for authenticated routes.
- Always clean up ECharts instances on component unmount.
- Always clean up event listeners on unmount.

### Form Handling

- The survey form is fully dynamic — steps and questions come from the backend API.
- Use `useProgressiveForm` hook for all survey form state management.
- Supported input types: `dropdown`, `radio`, `checkbox`, `chips`, `cards`.
- Conditional visibility: check `visible_when` rules against current form data.
- Cascading dropdowns: District → RevenueDivision → Mandal → Village (clear child on parent change).
- Mobile number validation: 10 digits, starts with 6-9, no all-repeating digits, unique per submission.

### Services

- Base URL from `VITE_API_BASE_URL` env variable, default `http://localhost:8000`.
- All authenticated requests include `Authorization: Bearer <token>` header.
- Service methods return typed responses.
- Handle API errors gracefully; show user-friendly messages.

### Styling

- Bootstrap 5 utility classes for layout (Container, Row, Col).
- Custom CSS in `App.css` and `index.css` for component-specific styles.
- Glass-morphism effect on login page.
- Mobile-first responsive design.
- Language toggle only visible on the survey page.

---

## API Design Conventions

### URL Patterns

```
/api/auth/admin/login/          # Auth endpoints
/api/auth/admin/invite/
/api/auth/admin/activate/

/api/locations/districts/        # Location masters (public, lang param)
/api/locations/divisions/
/api/locations/mandals/
/api/locations/villages/

/api/survey/schema/              # Survey definition (public, lang param)
/api/survey/choices/
/api/survey/submit/
/api/survey/check-mobile/

/api/dashboard/summary/          # Dashboard charts (authenticated)
/api/dashboard/women-status/
/api/dashboard/area-type/
/api/dashboard/age-distribution/
/api/dashboard/aspirations/
/api/dashboard/top-interests/
/api/dashboard/training-areas-trends/
/api/dashboard/entrepreneur-funnel/
/api/dashboard/submission-mode/
/api/dashboard/district-priority/

/api/analytics/summary/          # Analytics (public, flexible aggregation)
/api/analytics/question/{id}/
/api/analytics/location-breakdown/
/api/analytics/time-series/
```

### Conventions

- All endpoints use trailing slashes.
- Internationalization via `?lang=te` query parameter (default: `en`).
- Filtering via query parameters: `?district_id=1`, `?level=mandal`, `?period=daily`.
- POST for create/submit operations, GET for reads.
- Response format: `{ data: [...] }` for lists, flat object for singles.
- Error responses: `{ "field_name": ["Error message"] }` or `{ "detail": "Error" }`.
- Rate limiting: 50/min anonymous, 100/min authenticated.

---

## Error Handling Guidelines

### Backend

- Use DRF's `ValidationError` and `serializers.ValidationError` for input validation.
- Return structured errors: `{ "field": ["message"] }`.
- Log exceptions with `logger.error()` / `logger.exception()` — never silently swallow errors in critical paths.
- Dashboard aggregation methods return `[]` on exception (graceful degradation for charts).
- Email sending logs failures but does not raise (non-blocking).

### Frontend

- Wrap API calls in try/catch. Show user-friendly error messages.
- Use `loading` and `error` states from hooks for UI feedback.
- Show `LoadingSpinner` during async operations.
- Handle 401 responses by redirecting to login.
- Validate form fields before submission; show Bootstrap validation feedback.

---

## Code Review Expectations

- No hardcoded secrets, API URLs, or credentials.
- No N+1 queries — use `select_related` / `prefetch_related`.
- All new API endpoints must specify `permission_classes`.
- All new models must be registered in `api/models/__init__.py` and have migrations.
- All new frontend strings must be added to `translations.ts` for both `en` and `te`.
- Form fields must handle the `visible_when` conditional logic.
- Chart components must dispose ECharts instances on unmount.
- Mobile validation must enforce 10-digit, 6-9 start, no repeating digits.
- Survey answers must be validated against the active options whitelist.
- Location references must validate the full hierarchy chain.
