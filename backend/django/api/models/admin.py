import uuid

from django.contrib.auth.models import User
from django.db import models

class Admin(models.Model):
    """Extends Django User for Admin-specific metadata"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="admin_profile",
    )

    full_name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=15, blank=False, null=False)
    location = models.CharField(max_length=255, blank=False, null=False)
    note = models.TextField(max_length=500, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_super_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class AdminInvite(models.Model):
    """Invite flow model for admins"""

    invite_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=15, blank=False, null=False)
    location = models.CharField(max_length=255, blank=False, null=False)
    note = models.TextField(max_length=500, blank=True, null=True)

    invited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_admin_invites",
    )

    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
