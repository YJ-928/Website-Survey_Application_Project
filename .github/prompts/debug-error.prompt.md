---
description: Debug and fix an error or issue in the Survey Application.
tools: [vscode, execute, read, agent, edit, search, web, browser, 'com.figma.mcp/mcp/*', 'pylance-mcp-server/*', vscode.mermaid-chat-features/renderMermaidDiagram, ms-azuretools.vscode-containers/containerToolsConfig, ms-python.python/getPythonEnvironmentInfo, ms-python.python/getPythonExecutableCommand, ms-python.python/installPythonPackage, ms-python.python/configurePythonEnvironment, ms-toolsai.jupyter/configureNotebook, ms-toolsai.jupyter/listNotebookPackages, ms-toolsai.jupyter/installNotebookPackages, sonarsource.sonarlint-vscode/sonarqube_getPotentialSecurityIssues, sonarsource.sonarlint-vscode/sonarqube_excludeFiles, sonarsource.sonarlint-vscode/sonarqube_setUpConnectedMode, sonarsource.sonarlint-vscode/sonarqube_analyzeFile, todo]
---

# Debug Error

Diagnose and fix a bug or error in the Survey Application.

## Instructions

1. **Analyze the error** — read the error message, stack trace, or symptom description.
2. **Classify the error type**:
   - Backend 500/400 → check Django view, serializer, model
   - Frontend TypeScript error → check component, imports, types
   - API integration → check URL pattern mismatch, request/response shape, CORS
   - Auth failure (401) → check JWT token, permission_classes, header format
   - Empty data → check database queries, seed data, aggregation service
3. **Trace the code path** from the error location through the full stack.
4. **Read related files** — the view, serializer, model, service, and frontend component involved.
5. **Identify root cause** — is it a validation error, query issue, missing import, wrong URL, or config problem?
6. **Apply minimal fix** that follows project conventions.
7. **Run `get_errors`** to verify no new issues introduced.

## Common Issues Reference

| Error | Check |
|-------|-------|
| 404 on API call | URL trailing slash in both frontend service and `urls.py` |
| 401 Unauthorized | JWT token in localStorage, `authService.getAuthHeader()` |
| Empty chart | `aggregate_by_question()` in `api/services/dashboard.py`, question_id match |
| Survey field hidden | `visible_when` condition in form data, `useProgressiveForm` logic |
| Mobile rejected | 10-digit, starts 6-9, no repeating digits validation |
| Translation missing | Key in `translations.ts`, Telugu text in `data/translations_te.json` |
| N+1 performance | `select_related`/`prefetch_related` missing in queryset |
| Migration error | `python manage.py makemigrations` needed |

## Context Files to Check

- `backend/django/api/urls.py` — URL wiring
- `backend/django/backend/settings.py` — Django configuration
- `frontend/src/services/` — API service layer
- `frontend/src/hooks/useProgressiveForm.ts` — form state management
- `frontend/src/constants/translations.ts` — i18n strings
