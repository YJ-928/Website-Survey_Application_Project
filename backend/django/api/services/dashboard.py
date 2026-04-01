import logging
from django.db.models import Count

from api.models.survey import SurveyAnswer, SurveyQuestion

logger = logging.getLogger(__name__)


def aggregate_by_question(question_id: str):
    """
    Aggregate survey answers for a given question_id.
    Handles both single values and list values (for checkboxes).
    Safe for dashboards: never raises DoesNotExist.
    """

    try:
        question = SurveyQuestion.objects.filter(
            question_id=question_id
        ).first()

        if not question:
            logger.warning(
                "Dashboard aggregation skipped: question not found",
                extra={"question_id": question_id},
            )
            return []

        data = (
            SurveyAnswer.objects
            .filter(question=question)
            .values("value")
        )

        # Aggregate values, handling both single values and list values
        aggregated = {}
        for row in data:
            value = row["value"]
            
            # If value is a list (checkbox/multi-select), iterate through items
            if isinstance(value, list):
                for v in value:
                    aggregated[v] = aggregated.get(v, 0) + 1
            else:
                # Single value
                aggregated[value] = aggregated.get(value, 0) + 1

        return [
            {
                "label": label,
                "value": count,
            }
            for label, count in sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
        ]

    except Exception:
        logger.exception(
            "Dashboard aggregation failed",
            extra={"question_id": question_id},
        )
        return []
