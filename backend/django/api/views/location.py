import logging

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from api.models.location import (
    District,
    Mandal,
    RevenueDivision,
    Village,
)
from api.serializers.location import (
    DistrictSerializer,
    MandalSerializer,
    RevenueDivisionSerializer,
    VillageSerializer,
)

logger = logging.getLogger(__name__)

# Districts
class DistrictListView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        security=[],
        manual_parameters=[
            openapi.Parameter(
                "lang",
                openapi.IN_QUERY,
                description="Language code: 'en' for English, 'te' for Telugu (default: 'en')",
                type=openapi.TYPE_STRING,
                required=False,
            )
        ],
        operation_summary="List Districts",
        tags=["Location"],
    )
    def get(self, request, *args, **kwargs):
        language = request.query_params.get("lang", "en")
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'language': language})

        if not serializer.data:
            return Response(
                {
                    "data": [],
                    "message": "No district data found in Database",
                },
                status=200,
            )

        return Response(
            {
                "data": serializer.data,
                "message": "success",
            },
            status=status.HTTP_200_OK,
        )


# Revenue Divisions (Filtered by District)
class RevenueDivisionListView(ListAPIView):
    serializer_class = RevenueDivisionSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        security=[],
        manual_parameters=[
            openapi.Parameter(
                "district_id",
                openapi.IN_QUERY,
                description="District ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "lang",
                openapi.IN_QUERY,
                description="Language code: 'en' for English, 'te' for Telugu (default: 'en')",
                type=openapi.TYPE_STRING,
                required=False,
            )
        ],
        operation_summary="List Revenue Divisions",
        tags=["Location"],
    )
    def get(self, request, *args, **kwargs):
        district_id = request.query_params.get("district_id")
        language = request.query_params.get("lang", "en")

        if not district_id:
            return Response(
                {"detail": "district_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = RevenueDivision.objects.filter(
            district_id=district_id
        ).order_by("display_order")

        serializer = self.get_serializer(queryset, many=True, context={'language': language})

        if not serializer.data:
            return Response(
                {
                    "data": [],
                    "message": f"No revenue division data found for District_ID: {district_id}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "data": serializer.data,
                "message": "success",
            },
            status=status.HTTP_200_OK,
        )


# Mandals (Filtered by Revenue Division)
class MandalListView(ListAPIView):
    serializer_class = MandalSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        security=[],
        manual_parameters=[
            openapi.Parameter(
                "division_id",
                openapi.IN_QUERY,
                description="Revenue Division ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "lang",
                openapi.IN_QUERY,
                description="Language code: 'en' for English, 'te' for Telugu (default: 'en')",
                type=openapi.TYPE_STRING,
                required=False,
            )
        ],
        operation_summary="List Mandals",
        tags=["Location"],
    )
    def get(self, request, *args, **kwargs):
        division_id = request.query_params.get("division_id")
        language = request.query_params.get("lang", "en")

        if not division_id:
            return Response(
                {"detail": "division_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Mandal.objects.filter(
            division_id=division_id
        ).order_by("display_order")

        serializer = self.get_serializer(queryset, many=True, context={'language': language})

        if not serializer.data:
            return Response(
                {
                    "data": [],
                    "message": f"No mandal data found for given Division_ID:{division_id}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "data": serializer.data,
                "message": "success",
            },
            status=status.HTTP_200_OK,
        )


# Villages (Filtered by Mandal)
class VillageListView(ListAPIView):
    serializer_class = VillageSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        security=[],
        manual_parameters=[
            openapi.Parameter(
                "mandal_id",
                openapi.IN_QUERY,
                description="Mandal ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "lang",
                openapi.IN_QUERY,
                description="Language code: 'en' for English, 'te' for Telugu (default: 'en')",
                type=openapi.TYPE_STRING,
                required=False,
            )
        ],
        operation_summary="List Villages",
        tags=["Location"],
    )
    def get(self, request, *args, **kwargs):
        mandal_id = request.query_params.get("mandal_id")
        language = request.query_params.get("lang", "en")

        if not mandal_id:
            return Response(
                {"detail": "mandal_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = Village.objects.filter(
            mandal_id=mandal_id
        ).order_by("display_order")

        serializer = self.get_serializer(queryset, many=True, context={'language': language})

        if not serializer.data:
            return Response(
                {
                    "data": [],
                    "message": f"No village data found for given Mandal_ID:{mandal_id}",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "data": serializer.data,
                "message": "success",
            },
            status=status.HTTP_200_OK,
        )
