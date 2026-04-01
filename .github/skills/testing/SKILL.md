---
name: testing
description: Step-by-step reasoning for writing and running tests in the Survey Application project.
---

# Testing Skill

Use this reasoning pattern when writing or running tests for the Survey Application.

## Step 1: Identify What to Test

| Layer | What to Test | Framework |
|-------|-------------|-----------|
| **Models** | Field types, relationships, constraints, `__str__` | Django TestCase |
| **Serializers** | Validation logic, i18n output, read/write separation | DRF test utilities |
| **Views** | HTTP status codes, permissions, response format | DRF APITestCase + APIClient |
| **Services** | Business logic, aggregation, error handling | Django TestCase |
| **Frontend components** | Rendering, user interactions, state changes | React Testing Library (if configured) |
| **Integration** | End-to-end API workflows | DRF APITestCase |

## Step 2: Set Up Test Data

### Django Test Factories
```python
from django.test import TestCase
from api.models import District, RevenueDivision, Mandal, Village

class BaseTestCase(TestCase):
    def setUp(self):
        self.district = District.objects.create(name="Nalgonda", code="NLG")
        self.division = RevenueDivision.objects.create(
            district=self.district, division_code="NLG01", division_name="Nalgonda", display_order=1
        )
        self.mandal = Mandal.objects.create(
            division=self.division, mandal_code="NLG01M01", mandal_name="Nalgonda", display_order=1
        )
        self.village = Village.objects.create(
            mandal=self.mandal, village_code="NLG01M01V01", village_name="Test Village", display_order=1
        )
```

### Authenticated Requests
```python
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Admin

class AuthenticatedTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test@example.com", email="test@example.com", password="testpass")
        Admin.objects.create(user=self.user, full_name="Test Admin", is_active=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
```

## Step 3: Write Tests

### Model Tests
- Verify field constraints (unique, max_length)
- Test `__str__` returns expected string
- Test ForeignKey `PROTECT`/`CASCADE` behavior
- Test unique_together constraints

### Serializer Tests
- Valid input produces correct output
- Invalid input raises `ValidationError` with expected field errors
- i18n: test `?lang=te` returns Telugu text
- Survey submission: test mobile validation, location hierarchy, visible_when logic, option whitelisting

### View Tests
- `AllowAny` endpoints accessible without auth
- `IsAuthenticated` endpoints return 401 without token
- Correct response format: `{ data: [...] }` for lists
- Proper HTTP status codes: 200, 201, 400, 401, 404
- Query params applied: `?lang=te`, `?district_id=1`, `?level=mandal`

### Service Tests
- `aggregate_by_question()` returns correct counts
- `aggregate_by_question()` returns `[]` on exception
- `send_admin_invite_email()` logs failures without raising

## Step 4: Run Tests

```bash
# Run all tests
cd backend/django && python manage.py test

# Run specific app
python manage.py test api

# Run specific test class
python manage.py test api.tests.TestSurveySubmission

# Run with verbosity
python manage.py test --verbosity=2
```

## Step 5: Validate Test Quality

- Tests should be independent (each test sets up its own data).
- Use `setUp` and `tearDown` for common fixtures.
- Test both success and failure paths.
- Verify edge cases: empty data, boundary values, unicode text (Telugu).
- Ensure location hierarchy validations cover mismatched relationships.
- Mock external services (email) to avoid side effects.
