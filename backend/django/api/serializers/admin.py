import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

from api.models.admin import Admin, AdminInvite
from api.utils.decrypt import decrypt_password

logger = logging.getLogger(__name__)

class AdminLoginSerializer(serializers.Serializer):
    """Serializer to validate and generate token for Admins"""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        encrypted_password = data["password"]

        try:
            password = decrypt_password(encrypted_password)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

        user = authenticate(
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid email or password"
            )

        if not user.is_active or not user.is_staff:
            raise serializers.ValidationError(
                "User is not allowed to login"
            )

        refresh = RefreshToken.for_user(user)
        try:
            admin = user.admin_profile
        except Exception as e:
            logger.exception(f"No Admin Profile Found for User. Exception: {e}")

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.id,
            "email": user.email,
            "full_name": admin.full_name,
            "mobile": admin.mobile,
            "location": admin.location,
            "is_super_admin": admin.is_super_admin,
        }


class AdminInviteSerializer(serializers.ModelSerializer):
    """Serializer to validate and create an admin invite"""

    class Meta:
        model = AdminInvite
        fields = (
            "email",
            "full_name",
            "mobile",
            "location",
            "note",
        )

    def create(self, validated_data):
        request = self.context["request"]

        return AdminInvite.objects.create(
            **validated_data,
            invited_by=request.user,
            expires_at=timezone.now() + timedelta(days=2),
        )


class AdminActivateSerializer(serializers.Serializer):
    """Serializer to create password and complete admin registration"""
    invite_id = serializers.UUIDField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            invite = AdminInvite.objects.get(
                invite_id=data["invite_id"],
                is_used=False,
                expires_at__gt=timezone.now(),
            )
        except AdminInvite.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired invite")

        # Guard against duplicate users
        if User.objects.filter(username=invite.email).exists():
            raise serializers.ValidationError(
                "User already registered. Please login."
            )

        data["invite"] = invite
        return data

    def create(self, validated_data):
        invite = validated_data["invite"]

        with transaction.atomic():
            user = User.objects.create_user(
                username=invite.email,
                email=invite.email,
                password=validated_data["password"],
                is_staff=True,
                is_active=True,
            )

            Admin.objects.create(
                user=user,
                full_name=invite.full_name,
                mobile=invite.mobile,
                location=invite.location,
                note=invite.note,
                is_active=True,
                is_super_admin=False,
            )

            invite.is_used = True
            invite.save(update_fields=["is_used"])

        return user
