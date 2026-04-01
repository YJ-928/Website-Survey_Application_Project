import logging

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction

logger = logging.getLogger(__name__)


def create_default_super_admin(sender=None, **kwargs):
    """Create or repair the default super admin after migrations"""

    try:
        # Lazy import (apps ready)
        from api.models.admin import Admin

        User = get_user_model()

        email = getattr(settings, "DEFAULT_SUPER_ADMIN_EMAIL", None)
        password = getattr(settings, "DEFAULT_SUPER_ADMIN_PASSWORD", None)
        full_name = getattr(settings, "DEFAULT_SUPER_ADMIN_NAME", "Super Admin")
        mobile = getattr(settings, "DEFAULT_SUPER_ADMIN_MOBILE", "NA")
        location = getattr(settings, "DEFAULT_SUPER_ADMIN_LOCATION", "System")

        if not email or not password:
            logger.warning(
                "Default super admin credentials not configured; skipping creation"
            )
            return

        with transaction.atomic():
            # Ensure User exists
            user, user_created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "is_staff": True,
                    "is_superuser": True,
                },
            )

            if user_created:
                user.set_password(password)
                user.save()
                logger.info(
                    "Default super admin user created",
                    extra={"email": email},
                )

            # Ensure Admin profile exists
            admin, admin_created = Admin.objects.get_or_create(
                user=user,
                defaults={
                    "full_name": full_name,
                    "mobile": mobile,
                    "location": location,
                    "note": "System generated super admin",
                    "is_active": True,
                    "is_super_admin": True,
                },
            )

            if admin_created:
                logger.info(
                    "Admin profile created for default super admin",
                    extra={"email": email},
                )

        logger.info(
            "Default super admin verified successfully",
            extra={
                "email": email,
                "user_created": user_created,
                "admin_created": admin_created,
            },
        )

    except Exception:
        logger.exception(
            "Failed to create or verify default super admin during post_migrate"
        )
