import json
import logging
from django.db import transaction
from django.conf import settings

logger = logging.getLogger(__name__)


def seed_survey_schema_data(sender=None, **kwargs):
    """
    Seed survey schema (choices, steps, questions).
    Idempotent and safe to run multiple times.
    """

    try:
        from api.models.choice import ChoiceCategory, ChoiceOption
        from api.models.survey import SurveyStep, SurveyQuestion

        schema_path = settings.BASE_DIR / "data/survey_schema_v1.json"

        with open(schema_path, "r") as f:
            schema = json.load(f)

        with transaction.atomic():

            # ------------------------------------
            # Choice Categories & Options
            # ------------------------------------
            for category_data in schema.get("choice_categories", []):
                category, _ = ChoiceCategory.objects.get_or_create(
                    code=category_data["code"],
                    defaults={"name": category_data["name"]},
                )

                for option in category_data.get("options", []):
                    ChoiceOption.objects.update_or_create(
                        category=category,
                        code=option["code"],
                        defaults={
                            "label": option["label"],
                            "icon": option.get("icon"),
                            "display_order": option["order"],
                            "is_active": True,
                        },
                    )

            # ------------------------------------
            # Survey Steps & Questions
            # ------------------------------------
            for step_data in schema.get("steps", []):
                step, _ = SurveyStep.objects.get_or_create(
                    step_id=step_data["step_id"],
                    defaults={
                        "title": step_data["title"],
                        "step_number": step_data["step_number"],
                        "total_steps": step_data["total_steps"],
                    },
                )

                for q in step_data.get("questions", []):
                    category = None
                    if q.get("options_category"):
                        category = ChoiceCategory.objects.filter(
                            code=q["options_category"]
                        ).first()

                    SurveyQuestion.objects.get_or_create(
                        question_id=q["question_id"],
                        defaults={
                            "step": step,
                            "label": q["label"],
                            "input_type": q["input_type"],
                            "required": q["required"],
                            "options_category": category,
                            "visible_when": q.get("visible_when"),
                        },
                    )

        logger.info("Survey schema seeded successfully")

    except Exception:
        logger.exception("Failed to seed survey schema")
        raise
