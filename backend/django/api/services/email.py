import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_admin_invite_email(
    *,
    to_email: str,
    invite_link: str,
    full_name: str,
    mobile: str,
    location: str,
    note: str | None = None,
):
    """Send admin dashboard invite email"""

    try:
        subject = "Women Empowerment Admin Dashboard Invitation"

        html_content = render_to_string(
            "emails/admin_invite.html",
            {
                "invite_link": invite_link,
                "full_name": full_name,
                "email": to_email,
                "mobile": mobile,
                "location": location,
                "note": note,
            },
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=(
                "You have been invited to join the Women Empowerment "
                "Survey Admin Portal."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        logger.info(
            "Admin invite email sent successfully",
            extra={"email": to_email},
        )

    except Exception:
        logger.exception(
            "Failed to send admin invite email",
            extra={
                "email": to_email,
                "invite_link": invite_link,
            },
        )
