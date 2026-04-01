---
name: debugging
description: Systematic debugging reasoning for tracing and fixing issues in the Survey Application project.
---

# Debugging Skill

Use this reasoning pattern when diagnosing and fixing bugs in the Survey Application.

## Step 1: Classify the Error

| Error Type | Symptoms | Start Investigation |
|-----------|----------|---------------------|
| **Backend 500** | Server error response | Django logs, view code, serializer validation |
| **Backend 400** | Validation error | Serializer validation logic, request payload |
| **Frontend compile** | TypeScript error | `get_errors`, component imports, type definitions |
| **Frontend runtime** | UI crash or blank page | Console errors, component lifecycle, context providers |
| **API integration** | Wrong data or 404 | URL mismatch, request/response shape, CORS |
| **Auth failure** | 401 Unauthorized | JWT token expiry, header format, permission classes |
| **Data issue** | Wrong or missing data | Model queries, serializer output, seed data |

## Step 2: Reproduce and Trace

### Backend Path
```
Request → urls.py → View → Serializer → Model/Service → Response
```

1. Is the URL wired in `api/urls.py`?
2. Does the view have correct `permission_classes`?
3. Does the serializer validate correctly? Check `validate_*` methods.
4. Does the query use proper joins? Check for N+1 with `select_related`/`prefetch_related`.
5. Does the service method handle exceptions? Check for bare `except:` clauses.

### Frontend Path
```
User action → Component → Service → fetch() → Response → State → Re-render
```

1. Is the service method calling the correct URL (with trailing slash)?
2. Is the auth header included for protected endpoints?
3. Is the response being parsed correctly (check `.data` vs direct array)?
4. Is state being updated properly via Context or local state?
5. Are cleanup functions running on unmount?

### Integration Path
```
Frontend Service → HTTP Request → CORS → Django View → Serializer → Response → Frontend Parse
```

1. Does the request URL match the backend URL pattern exactly (including trailing slash)?
2. Does the request body match the serializer's expected fields?
3. Does the response shape match what the frontend expects?
4. Is CORS configured for the frontend origin?
5. Is `?lang=te` passed where needed?

## Step 3: Common Root Causes

### Survey Submission Failures
- Mobile number validation: must be 10 digits, start with 6-9, no all-repeating digits, unique
- Location hierarchy: village's mandal must match submitted mandal, etc.
- Required field missing: check `visible_when` — field may be conditionally required
- Option not in whitelist: answer value must be in active `ChoiceOption` for that category

### Dashboard/Analytics Empty Data
- `aggregate_by_question()` returns `[]` on any exception — check logs
- Question ID mismatch between frontend request and backend survey schema
- No survey submissions in database — check seed data flag `SEED_DATA` env var

### Authentication Issues
- Token expired: access=60min, refresh=7min — check `SIMPLE_JWT` settings
- Wrong algorithm: must be RS256, check key files exist at configured paths
- Password decryption: RSA-OAEP key pair must match between frontend public key and backend private key

### Translation Issues
- Missing key in `translations.ts` — check for typos in key name
- Backend returns English regardless — check `?lang=te` is passed to serializer context
- `translate()` returns original text — check `data/translations_te.json` has the mapping

## Step 4: Apply Fix

1. Make the **minimal change** that resolves the issue.
2. Check for side effects in related files.
3. Run `get_errors` to verify no new issues.
4. If model changed: create migration.
5. If translation added: add both `en` and `te`.
6. If URL changed: update both backend `urls.py` and frontend service.
