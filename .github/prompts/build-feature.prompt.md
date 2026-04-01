---
model: Claude Sonnet 4.6 (copilot)
description: Build a new feature for the Survey Application spanning backend and frontend.
tools:
  - read_file
  - grep_search
  - file_search
  - semantic_search
  - create_file
  - replace_string_in_file
  - run_in_terminal
---

# Build Feature

Implement a new feature for the Survey Application. This covers the full stack: database model, API endpoint, frontend service, UI component, and translations.

## Instructions

### Phase 1: Backend
1. **Model** (if needed) — create in `api/models/`, register in `api/models/__init__.py`, create migration.
2. **Serializer** — create in `api/serializers/`. Support `language` context for i18n.
3. **View** — create in `api/views/`. Set `permission_classes`. Use `select_related`/`prefetch_related`.
4. **URL** — import new view at top of `api/urls.py` and add path with trailing slash.
5. **Service** (if complex logic) — add to `api/services/`.

### Phase 2: Frontend
6. **Service method** — add to appropriate file in `src/services/`.
7. **Component** — create in `src/UI/Auth/` (protected) or `src/UI/PreAuth/` (public). Use functional components with hooks.
8. **Route** (if new page) — add to `src/App.tsx`. Use `ProtectedRoute` for admin pages.
9. **Translations** — add all UI strings to `src/constants/translations.ts` for both `en` and `te`.
10. **Styling** — use Bootstrap 5 classes and React Bootstrap components.

### Phase 3: Integration
11. Verify request/response shapes match between frontend service and backend serializer.
12. Ensure `?lang=te` parameter works for i18n endpoints.
13. For charts: use ECharts components from `src/shared/charts/` with `{ name: string; value: number }[]` data format.

## Context Files to Read First

- `backend/django/api/urls.py` — URL patterns
- `frontend/src/App.tsx` — routing
- `frontend/src/constants/translations.ts` — i18n keys
- Similar existing feature files for pattern reference
