---
name: api-design
description: Step-by-step reasoning for designing REST API endpoints in the Survey Application project.
---

# API Design Skill

Use this reasoning pattern when designing a new REST API endpoint for the Survey Application.

## Step 1: Define the Contract

1. **Purpose**: What does this endpoint do? (CRUD, aggregation, validation)
2. **HTTP Method**: GET for reads, POST for creates/submits
3. **URL Pattern**: Follow `/api/{domain}/{resource}/` with trailing slash
4. **Access**: `AllowAny` (public) or `IsAuthenticated` (admin dashboard)
5. **I18n**: Does the response contain user-facing text that needs `?lang=te` support?

## Step 2: Design Request/Response

**Request:**
- Query parameters for GET: `?lang=en`, `?district_id=1`, `?level=mandal`, `?period=daily`
- JSON body for POST: `{ field: value }`

**Response:**
- List: return array or `{ data: [...] }`
- Single: return flat object `{ field: value }`
- Error: `{ "field_name": ["Error message"] }` or `{ "detail": "Error" }`
- Status codes: 200 (success), 201 (created), 400 (validation), 401 (unauth), 404 (not found)

## Step 3: Implement Backend

1. **Model** — does the existing model support this? If not, design the model change first.
2. **Serializer** — create in `api/serializers/`. Read serializer for GET, write serializer for POST. Pass `language` through context.
3. **View** — create in `api/views/`. Set `permission_classes`. Pass `lang` param to serializer context.
4. **URL** — import view at top of `api/urls.py` and add path with trailing slash.
5. **Register models** — new models must be added to `api/models/__init__.py`. Views and serializers are imported directly in `api/urls.py` (their `__init__.py` files are intentionally empty).

## Step 4: Implement Frontend

1. **Service method** — add to appropriate service in `src/services/`.
2. **Type definitions** — define request/response types.
3. **Auth headers** — include `authService.getAuthHeader()` for authenticated endpoints.
4. **Error handling** — try/catch with user-friendly error messages.

## Step 5: Validate

- Run `python manage.py check` for Django issues.
- Verify URL is accessible via Swagger at `/swagger/`.
- Check i18n: does `?lang=te` return Telugu text?
- Ensure `select_related`/`prefetch_related` used for related data.
- Confirm rate limiting: 50/min anon, 100/min authenticated.
