import logging

from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from api.models.survey import SurveySubmission, SurveyAnswer, SurveyQuestion
from api.services.dashboard import aggregate_by_question

logger = logging.getLogger(__name__)

# ---------------------------------------------
# Common Swagger Schemas
# ---------------------------------------------

CHART_RESPONSE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "label": openapi.Schema(type=openapi.TYPE_STRING),
            "value": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
    ),
)

SUMMARY_RESPONSE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "total_responses": openapi.Schema(type=openapi.TYPE_INTEGER),
        "completed_surveys": openapi.Schema(type=openapi.TYPE_INTEGER),
    },
)

# ---------------------------------------------
# Dashboard Summary
# ---------------------------------------------

class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: SUMMARY_RESPONSE_SCHEMA},
        operation_summary="Dashboard Summary",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            total = SurveySubmission.objects.count()
            completed = SurveySubmission.objects.filter(
                is_complete=True
            ).count()

            logger.info(
                "Dashboard summary fetched",
                extra={"admin_id": request.user.id},
            )

            return Response(
                {
                    "total_responses": total,
                    "completed_surveys": completed,
                },
                status=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception(
                "Dashboard summary failed",
                extra={"admin_id": request.user.id},
            )
            return Response(
                {
                    "total_responses": 0,
                    "completed_surveys": 0,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

# ---------------------------------------------
# Generic Question-based Charts
# ---------------------------------------------

class WomenStatusChartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: CHART_RESPONSE_SCHEMA},
        operation_summary="Women Status Chart",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            return Response(
                aggregate_by_question("EMPLOYMENT_STATUS"),
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Women status chart failed")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AreaTypeChartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: CHART_RESPONSE_SCHEMA},
        operation_summary="Area Type Split",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            return Response(
                aggregate_by_question("AREA_TYPE"),
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Area type chart failed")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AgeDistributionChartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: CHART_RESPONSE_SCHEMA},
        operation_summary="Age Distribution",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            return Response(
                aggregate_by_question("AGE_GROUP"),
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Age distribution chart failed")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AspirationsChartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: CHART_RESPONSE_SCHEMA},
        operation_summary="Aspirations",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            return Response(
                aggregate_by_question("INTERESTS"),
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Aspirations chart failed")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TopInterestsChartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: CHART_RESPONSE_SCHEMA},
        operation_summary="Top Interests",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            return Response(
                aggregate_by_question("INTERESTS"),
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Top interests chart failed")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TrainingAreasTimeSeriesView(APIView):
    """
    GET /api/dashboard/training-areas-trends/
    Returns training areas broken down by submission date (last 7 days)
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "categories": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                "series": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "data": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER))
                    }
                ))
            }
        )},
        operation_summary="Training Areas Time Series",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            from datetime import datetime, timedelta
            from django.utils import timezone
            
            # Get last 7 days
            today = timezone.now().date()
            dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]
            
            # Get the training areas question
            question = SurveyQuestion.objects.filter(question_id="TRAINING_AREAS").first()
            
            if not question:
                return Response({
                    "categories": [d.strftime("%a") for d in dates],
                    "series": []
                }, status=status.HTTP_200_OK)
            
            # Get all training answers
            all_answers = SurveyAnswer.objects.filter(question=question)
            
            # Collect all unique training areas from list values
            unique_areas = set()
            for answer in all_answers:
                value = answer.value
                if isinstance(value, list):
                    unique_areas.update(value)
                else:
                    unique_areas.add(value)
            
            if not unique_areas:
                return Response({
                    "categories": [d.strftime("%a") for d in dates],
                    "series": []
                }, status=status.HTTP_200_OK)
            
            # Build series data for each training area
            series = []
            for area in sorted(unique_areas):
                area_data = []
                for date in dates:
                    # Count submissions where TRAINING_AREAS contains this area
                    count = 0
                    for answer in all_answers.filter(submission__created_at__date=date):
                        value = answer.value
                        if isinstance(value, list) and area in value:
                            count += 1
                        elif isinstance(value, str) and value == area:
                            count += 1
                    area_data.append(count)
                
                series.append({
                    "name": area,
                    "data": area_data
                })
            
            return Response({
                "categories": [d.strftime("%a") for d in dates],
                "series": series
            }, status=status.HTTP_200_OK)
            
        except Exception:
            logger.exception("Training areas trends chart failed")
            return Response({
                "categories": [],
                "series": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EntrepreneurFunnelView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: CHART_RESPONSE_SCHEMA},
        operation_summary="Entrepreneur Funnel",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            return Response(
                aggregate_by_question("ENTREPRENEUR_STAGE"),
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Entrepreneur funnel chart failed")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmissionModeChartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: CHART_RESPONSE_SCHEMA},
        operation_summary="Submission Mode",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            return Response(
                aggregate_by_question("SUBMISSION_MODE"),
                status=status.HTTP_200_OK,
            )
        except Exception:
            logger.exception("Submission mode chart failed")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ---------------------------------------------
# District Priority
# ---------------------------------------------

class DistrictPriorityView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        security=[{"Bearer": []}],
        responses={200: CHART_RESPONSE_SCHEMA},
        operation_summary="Mandal Priority Index",
        tags=["Dashboard"],
    )
    def get(self, request):
        try:
            data = (
                SurveySubmission.objects
                .values("mandal__mandal_name")
                .annotate(value=Count("mandal_id"))
                .order_by("-value")
            )

            return Response(
                [
                    {"label": row["mandal__mandal_name"], "value": row["value"]}
                    for row in data
                ],
                status=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception("Mandal priority chart failed")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
