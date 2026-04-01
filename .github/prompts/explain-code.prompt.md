---
description: Explain how a specific part of the Survey Application codebase works.
tools:
  - read_file
  - grep_search
  - file_search
  - semantic_search
---

# Explain Code

Explain how a specific part of the Survey Application works. Trace the full data flow from user action through frontend components, API service calls, backend views, serializers, models, and database.

## Instructions

1. **Identify the feature** — determine which files and layers are involved.
2. **Read all relevant files** in the data flow path:
   - Frontend: component → service → context/hook
   - Backend: URL → view → serializer → model → service/util
3. **Explain the flow** step by step with code references.
4. **Highlight key decisions**: validation rules, i18n handling, query optimization, conditional logic.
5. **Note any dependencies**: environment variables, external services, seed data.

## Key Flows to Be Aware Of

- **Survey submission**: MobileVerification → SurveyForm → useProgressiveForm → formService.submitSurvey → SubmitSurveyView (`api/views/survey_submit.py`) → SurveySubmissionCreateSerializer → SurveySubmission + SurveyAnswer (bulk_create)
- **Admin login**: Login component → authService.login (RSA encrypt password) → AdminLoginView (`api/views/admin.py`) → AdminLoginSerializer (decrypt + authenticate + JWT)
- **Dashboard charts**: Admin component → analyticsService / direct dashboard fetch → DashboardView (`api/views/dashboard.py`) → dashboard service (`api/services/dashboard.py`: aggregate_by_question) → Chart component
- **Location cascade**: DropdownField (district) → locationService → DropdownField (division) → locationService → etc.
- **i18n**: LanguageContext → `?lang=te` param → serializer context → translate() utility (`api/utils/translate.py`)
- **Survey schema**: SurveyForm init → formService.getSurveySchema → SurveySchemaView (`api/views/survey_schema.py`) → SurveyStepSerializer
