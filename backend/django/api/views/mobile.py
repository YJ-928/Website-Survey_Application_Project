from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import SurveySubmission
from api.serializers.mobile import MobileCheckSerializer


class SurveyMobileCheckView(APIView):
    """Check if a mobile number has already submitted the survey"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Check survey submission by mobile number",
        operation_description=(
            "Checks whether a given mobile number has already "
            "submitted the survey. If found, returns the survey "
        ),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["mobile_number"],
            properties={
                "mobile_number": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="9876543210",
                    description="10-digit Indian mobile number"
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Mobile number check result",
                examples={
                    "application/json": {
                        "exists_true": {
                            "exists": True,
                            "message": "Survey already submitted"
                        },
                        "exists_false": {
                            "exists": False,
                            "message": "Mobile number not found"
                        }
                    }
                },
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "exists": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN
                        ),
                        "reference_id": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            nullable=True
                        ),
                        "message": openapi.Schema(
                            type=openapi.TYPE_STRING
                        ),
                    }
                ),
            ),
            400: openapi.Response(
                description="Invalid mobile number",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "mobile_number": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_STRING,
                                example="Mobile number must be 10 digits"
                            )
                        )
                    }
                ),
            ),
        },
        tags=["Survey"],
    )
    def post(self, request):
        serializer = MobileCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile_number"]

        # Use exists() for better performance - doesn't fetch the object
        submission_exists = SurveySubmission.objects.filter(
            mobile_number=mobile
        ).exists()

        if submission_exists:
            return Response(
                {
                    "exists": True,
                    "message": "Survey already submitted",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "exists": False,
                "message": "Mobile number not found",
            },
            status=status.HTTP_200_OK,
        )
