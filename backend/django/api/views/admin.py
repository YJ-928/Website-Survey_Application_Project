import logging

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.services.email import send_admin_invite_email
from api.serializers.admin import AdminActivateSerializer, AdminInviteSerializer, AdminLoginSerializer

logger = logging.getLogger(__name__)


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=AdminLoginSerializer,
        security=[],
        responses={
            200: openapi.Response(
                description="JWT access and refresh tokens"
            )
        },
        operation_summary="Admin Login",
        operation_description="Admin login using RSA encrypted password",
        tags=["Auth"],
    )
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class AdminInviteView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AdminInviteSerializer,
        security=[{"Bearer": []}],
        responses={
            200: openapi.Response(description="Admin invited successfully")
        },
        operation_summary="Invite Admin",
        operation_description="Admin invites a user via email",
        tags=["Auth"],
    )
    def post(self, request):
        try:
            serializer = AdminInviteSerializer(
                data=request.data,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            invite = serializer.save()

            invite_link = (
                f"{settings.FRONTEND_BASE_URL}"
                f"{settings.FRONTEND_INVITE_PATH}"
                f"?invite_id={invite.invite_id}"
            )

            send_admin_invite_email(
                to_email=invite.email,
                invite_link=invite_link,
                full_name=invite.full_name,
                mobile=invite.mobile,
                location=invite.location,
                note=invite.note,
            )

            logger.info(
                "Admin invited",
                extra={
                    "email": invite.email,
                    "invited_by": request.user.id,
                },
            )

            return Response(
                {"message": "Admin invited successfully"}
            )

        except Exception:
            logger.exception(
                "Admin invite failed",
                extra={"invited_by": request.user.id},
            )
            raise


class AdminActivateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=AdminActivateSerializer,
        security=[{"Bearer": []}],
        responses={
            200: openapi.Response(description="Admin account activated")
        },
        operation_summary="Activate Admin",
        operation_description="Activate user account using invite ID",
        tags=["Auth"],
    )
    def post(self, request):
        try:
            serializer = AdminActivateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            logger.info(
                "Admin activated",
                extra={"user_id": user.id},
            )

            return Response(
                {
                    "message": "Account activated successfully",
                    "user_id":user.id
                }
            )

        except Exception as exc:
            logger.exception(f"Expection occured: {exc}")
            return Response(
                {"message": "Something went wrong. Please try again later."},
                status=500,
            )

