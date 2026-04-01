import logging

from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from api.models.survey import SurveyStep, SurveyQuestion
from api.serializers.survey_schema import SurveyStepSerializer

logger = logging.getLogger(__name__)


class SurveySchemaView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: SurveyStepSerializer(many=True),
        },
        operation_summary="Get survey schema",
        operation_description="Returns survey steps and questions for FE rendering. Supports language parameter: ?lang=te for Telugu, ?lang=en for English (default)",
        tags=["Survey"],
        security=[],
    )
    def get(self, request):
        # Get language parameter from query string (default: 'en')
        language = request.query_params.get('lang', 'en')
        
        # Validate language parameter
        if language not in ['en', 'te']:
            language = 'en'
        
        steps = (
            SurveyStep.objects
            .prefetch_related(
                Prefetch(
                    "questions",
                    queryset=SurveyQuestion.objects.select_related(
                        "options_category"
                    ).order_by("order", "id"),
                )
            )
            .order_by("step_number")
        )

        if not steps.exists():
            logger.warning("Survey schema requested but no steps found")
            return Response(
                {"detail": "Survey schema not configured"},
                status=status.HTTP_200_OK,
            )

        return Response(
            SurveyStepSerializer(steps, many=True, context={'language': language}).data,
            status=status.HTTP_200_OK,
        )
