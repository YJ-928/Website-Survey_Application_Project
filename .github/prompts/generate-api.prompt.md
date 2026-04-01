---
description: Generate a new REST API endpoint end-to-end for the Survey Application project.
tools:
  - read_file
  - grep_search
  - file_search
  - create_file
  - replace_string_in_file
  - run_in_terminal
---

# Generate API Endpoint

Create a new REST API endpoint for the Survey Application. Implement the full stack: Django model (if needed), serializer, view, URL wiring, and frontend service method.

## Instructions

1. **Read existing patterns** by examining similar files in the same directory before writing code.
2. **Follow project conventions**:
   - URL: `/api/{domain}/{resource}/` with trailing slash
   - View: DRF `APIView` with explicit `permission_classes`
   - Serializer: separate read/write if needed, pass `language` context for i18n
   - Queries: use `select_related`/`prefetch_related` to prevent N+1
   - Response: `{ data: [...] }` for lists, flat object for singles
   - Status codes: 200, 201, 400, 401, 404
3. **Register** new models in `api/models/__init__.py`. Views and serializers don't need `__init__.py` registration.
4. **Wire** the URL in `api/urls.py` with the correct import at the top of the file.
5. **Create** the frontend service method in the appropriate `src/services/` file.
6. **Create** migration if model changes are needed: `python manage.py makemigrations`.

## Context Files to Read First

- `backend/django/api/urls.py` — existing URL patterns and import style
- The equivalent domain files (e.g., `api/views/dashboard.py` for a new dashboard endpoint)
- `api/models/__init__.py` — if adding new models
