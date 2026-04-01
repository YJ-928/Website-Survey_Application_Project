---
name: database-design
description: Step-by-step reasoning for designing and modifying database models in the Survey Application project.
---

# Database Design Skill

Use this reasoning pattern when designing or modifying Django models and database schema for the Survey Application.

## Step 1: Understand the Domain

The database has these entity groups:
- **Location hierarchy**: District → RevenueDivision → Mandal → Village (Nalgonda district)
- **Survey schema**: SurveyStep → SurveyQuestion → ChoiceCategory → ChoiceOption
- **Survey data**: SurveySubmission → SurveyAnswer
- **Admin management**: Admin (extends User), AdminInvite

## Step 2: Design the Model

### Field Type Selection
| Data Type | Django Field | Notes |
|-----------|-------------|-------|
| Short text | `CharField(max_length=N)` | Names, codes |
| Long text | `TextField` | Descriptions |
| Boolean | `BooleanField(default=False)` | Flags |
| Integer | `IntegerField` / `PositiveIntegerField` | Counts, order |
| Flexible data | `JSONField(default=dict)` | `visible_when`, answer values |
| UUID | `UUIDField(primary_key=True, default=uuid.uuid4)` | Submission IDs |
| Timestamp | `DateTimeField(auto_now_add=True)` | created_at |

### Relationship Rules
| Relationship | on_delete | When |
|-------------|-----------|------|
| Location hierarchy (Division→District, Mandal→Division, Village→Mandal) | `CASCADE` | Cascade deletes within the location tree |
| SurveySubmission → Location FKs | `PROTECT` | Prevent deleting locations referenced by submissions |
| Answer → Submission | `CASCADE` | Delete answers when submission deleted |
| Question → Step | `CASCADE` | Delete questions when step deleted |
| Question → ChoiceCategory | `SET_NULL, null=True` | Category removal shouldn't delete questions |
| ChoiceOption → ChoiceCategory | `CASCADE` | Delete options when category deleted |
| Admin → User | `CASCADE` | Admin profile tied to user |

### Required Conventions
- Every model needs a `__str__` method.
- Add `class Meta` with `ordering` where natural order exists.
- Add `db_index=True` on frequently queried fields.
- Use `unique=True` for natural identifiers (codes, reference IDs, mobile numbers).
- Use `unique_together` for composite uniqueness (e.g., `(category, code)` for ChoiceOption).

## Step 3: Create the Model File

1. Place in `api/models/` — one file per domain.
2. Import in `api/models/__init__.py` (this is the only `__init__.py` that needs updating; `api/views/__init__.py` and `api/serializers/__init__.py` are intentionally empty).
3. Follow existing patterns in `location.py`, `survey.py`, `choice.py`, `admin.py`.

## Step 4: Create Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

- Never modify existing migrations.
- If adding to existing model, create a new migration file.
- For seed data, use post-migrate signals (controlled by `SEED_DATA` env flag).

## Step 5: Wire to Serializers and Views

1. Create serializer in `api/serializers/` if the model is exposed via API.
2. Pass `language` context for i18n fields.
3. Use `select_related` / `prefetch_related` in views to avoid N+1.
4. Use `transaction.atomic()` for multi-model write operations.
5. Use `bulk_create()` for inserting multiple records.

## Step 6: Validate

- Run `python manage.py check` for Django system checks.
- Run `python manage.py showmigrations` to verify migration state.
- Check that `PROTECT` relationships prevent unintended deletes.
- Verify indexes exist for fields used in filters and lookups.
