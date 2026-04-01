---
description: Review backend code changes in the Survey Application Django project for correctness, security, and conventions.
tools: [vscode, execute, read, agent, edit, search, web, browser, 'com.figma.mcp/mcp/*', 'pylance-mcp-server/*', vscode.mermaid-chat-features/renderMermaidDiagram, ms-azuretools.vscode-containers/containerToolsConfig, ms-python.python/getPythonEnvironmentInfo, ms-python.python/getPythonExecutableCommand, ms-python.python/installPythonPackage, ms-python.python/configurePythonEnvironment, ms-toolsai.jupyter/configureNotebook, ms-toolsai.jupyter/listNotebookPackages, ms-toolsai.jupyter/installNotebookPackages, sonarsource.sonarlint-vscode/sonarqube_getPotentialSecurityIssues, sonarsource.sonarlint-vscode/sonarqube_excludeFiles, sonarsource.sonarlint-vscode/sonarqube_setUpConnectedMode, sonarsource.sonarlint-vscode/sonarqube_analyzeFile, todo]
---

# Review Backend Code

Review Django backend code changes for the Survey Application project. Check for correctness, security, performance, and adherence to project conventions.

## Instructions

1. **Read all changed files** and their related files (e.g., the serializer that a view uses).
2. **Apply this checklist** to every change:

### Models
- [ ] Has `__str__` method
- [ ] ForeignKey on_delete: `PROTECT` for SurveySubmission→locations, `CASCADE` within location hierarchy and for answers, `SET_NULL` for optional category FKs
- [ ] Registered in `api/models/__init__.py`
- [ ] Migration created

### Serializers
- [ ] Validates inputs at serializer level (not in views)
- [ ] Passes `language` via `self.context.get('language', 'en')`
- [ ] Note: `api/serializers/__init__.py` is intentionally empty; imports go in `api/urls.py`

### Views
- [ ] Explicit `permission_classes` set
- [ ] `lang` query param passed to serializer context
- [ ] `select_related`/`prefetch_related` used (no N+1)
- [ ] Correct HTTP status codes (200, 201, 400, 401, 404)
- [ ] Imported at top of `api/urls.py` and path wired with trailing slash

### Security
- [ ] No hardcoded secrets or credentials
- [ ] No raw SQL (use ORM)
- [ ] Input validated at system boundary
- [ ] JWT RS256 only

### Performance
- [ ] No N+1 query patterns
- [ ] `bulk_create()` for batch inserts
- [ ] `transaction.atomic()` for multi-model writes
- [ ] Database indexes on frequently queried fields

3. **Report issues** with severity (Critical / Major / Minor), file path, and fix suggestion.
4. **Run `get_errors`** to verify no compile errors.
