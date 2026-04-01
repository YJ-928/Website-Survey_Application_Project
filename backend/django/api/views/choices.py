import logging

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from api.models.choice import ChoiceCategory
from api.serializers.choice import ChoiceCategorySerializer

logger = logging.getLogger(__name__)


class ChoiceListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "category",
                openapi.IN_QUERY,
                description="Choice category code (e.g. AGE_GROUP)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "lang",
                openapi.IN_QUERY,
                description="Language code: 'en' for English, 'te' for Telugu (default: 'en')",
                type=openapi.TYPE_STRING,
                required=False,
            )
        ],
        responses={
            200: ChoiceCategorySerializer(many=True),
            404: openapi.Response(description="Invalid category"),
        },
        operation_summary="List choice categories",
        operation_description="Returns enum categories and active options with translations",
        tags=["Survey Metadata"],
        security=[],
    )
    def get(self, request):
        category = request.GET.get("category")
        language = request.GET.get("lang", "en")
        
        # Validate language parameter
        if language not in ['en', 'te']:
            language = 'en'

        qs = ChoiceCategory.objects.prefetch_related("options")

        if category:
            qs = qs.filter(code=category)
            if not qs.exists():
                logger.warning(
                    "Invalid choice category requested",
                    extra={"category": category},
                )
                return Response(
                    {"detail": "Invalid choice category"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            ChoiceCategorySerializer(qs, many=True, context={'language': language}).data,
            status=status.HTTP_200_OK,
        )
