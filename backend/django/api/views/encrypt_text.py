from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.utils.encrypt import encrypt_to_hex


class EncryptTestView(APIView):
    """Internal View to encrypt plain text using RS-256 and Public Key"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["text"],
            properties={
                "text": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Plain text to encrypt",
                )
            },
        ),
        responses={
            200: openapi.Response(
                description="Encrypted hex string"
            )
        },
        security=[],
        operation_summary="Encrypt Test (Internal)",
        tags=["Internal"],
    )
    def post(self, request):
        plain_text = request.data.get("text")

        if not plain_text:
            return Response(
                {"error": "text is required"},
                status=400,
            )

        encrypted = encrypt_to_hex(plain_text)
        return Response({"encrypted": encrypted})
