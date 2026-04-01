---
name: code-review
description: Systematic code review reasoning for the Survey Application project.
---

# Code Review Skill

Use this reasoning pattern when reviewing code changes in the Survey Application.

## Step 1: Identify Scope

1. What files were changed?
2. Which layer is affected? Backend (Django), frontend (React), or both?
3. Is this a new feature, bug fix, or refactor?

## Step 2: Check Backend Code

### Models (`api/models/`)
- Has `__str__` method?
- ForeignKey `on_delete`: `PROTECT` for SurveySubmission→locations, `CASCADE` within location hierarchy and for answers, `SET_NULL` for optional category FKs?
- Indexed fields for common queries?
- Registered in `api/models/__init__.py`?
- Migration created via `makemigrations`?

### Serializers (`api/serializers/`)
- Separate read/write if shapes differ?
- Passes `language` from context: `self.context.get('language', 'en')`?
- Validation at serializer level (not view)?
- Note: `api/serializers/__init__.py` is intentionally empty; serializers are imported directly by path in `api/urls.py`.

### Views (`api/views/`)
- Has explicit `permission_classes`?
- Passes `lang` query param to serializer context?
- Uses `select_related`/`prefetch_related` for queries?
- Returns correct HTTP status code?
- Note: `api/views/__init__.py` is intentionally empty; views are imported directly by path in `api/urls.py`.

### URLs (`api/urls.py`)
- Trailing slash on all endpoints?
- Follows `/api/{domain}/{resource}/` pattern?
- New views imported at top of `urls.py`?

## Step 3: Check Frontend Code

### Components
- Functional component with hooks?
- In correct directory (`UI/Auth/` or `UI/PreAuth/`)?
- ECharts disposed on unmount?
- Event listeners cleaned up?

### Services (`src/services/`)
- Uses `API_BASE` from env?
- Auth header included for protected endpoints?
- Error handling with try/catch?

### Translations (`src/constants/translations.ts`)
- New UI strings added for both `en` and `te`?
- Uses `t(key, language)` function?

### Forms
- Dynamic `visible_when` logic respected?
- Cascading dropdowns clear child on parent change?
- Mobile validation: 10 digits, starts 6-9, no repeats?

## Step 4: Check Security

- No hardcoded secrets, API keys, or credentials?
- No raw SQL queries (use ORM)?
- Input validation at system boundary?
- CORS configuration appropriate?
- JWT RS256 only (never HS256)?

## Step 5: Check Performance

- No N+1 queries (use `select_related`/`prefetch_related`)?
- Batch inserts use `bulk_create()`?
- Multi-model writes wrapped in `transaction.atomic()`?
- Pagination for large result sets?

## Step 6: Report Findings

Categorize issues as:
- **Critical**: Security vulnerabilities, data loss risks
- **Major**: Bugs, performance issues, missing validation
- **Minor**: Style violations, convention deviations
- **Suggestion**: Optional improvements

Include file path, line reference, description, and suggested fix for each issue.
