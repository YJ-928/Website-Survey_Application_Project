import logging

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from api.serializers.survey_submission import (
    SurveySubmissionCreateSerializer,
    SurveySubmissionDetailSerializer,
)

logger = logging.getLogger(__name__)


class SubmitSurveyView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SurveySubmissionCreateSerializer,
        responses={
            201: SurveySubmissionDetailSerializer,
            400: openapi.Response(description="Validation error"),
        },
        operation_summary="Submit survey",
        operation_description="Submit anonymized survey response",
        tags=["Survey"],
        security=[],
    )
    def post(self, request):
        serializer = SurveySubmissionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission = serializer.save()

        logger.info(
            "Survey submitted successfully",
            extra={
                "reference_id": submission.reference_id,
                "district_id": submission.district_id,
            },
        )

        return Response(
            SurveySubmissionDetailSerializer(submission).data,
            status=status.HTTP_201_CREATED,
        )
