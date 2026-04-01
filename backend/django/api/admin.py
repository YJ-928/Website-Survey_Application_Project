from django.contrib import admin

from api.models.admin import Admin, AdminInvite
from api.models.location import District, Mandal, RevenueDivision, Village
from api.models.choice import ChoiceCategory, ChoiceOption
from api.models.survey import (
    SurveySubmission,
    SurveyAnswer,
    SurveyStep,
    SurveyQuestion,
)

# ADMIN PROFILES
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_email",
        "full_name",
        "mobile",
        "location",
        "is_active",
        "is_super_admin",
        "created_at",
    )

    search_fields = (
        "user__email",
        "full_name",
        "mobile",
    )

    list_filter = (
        "is_active",
        "is_super_admin",
    )

    readonly_fields = (
        "user",
        "created_at",
    )

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Email"
    get_email.admin_order_field = "user__email"

# ADMIN INVITES
@admin.register(AdminInvite)
class AdminInviteAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "mobile",
        "location",
        "invited_by_email",
        "is_used",
        "expires_at",
        "created_at",
    )

    search_fields = (
        "email",
        "full_name",
        "mobile",
    )

    list_filter = (
        "is_used",
        "expires_at",
    )

    readonly_fields = (
        "invite_id",
        "invited_by",
        "created_at",
    )

    def invited_by_email(self, obj):
        return obj.invited_by.email if obj.invited_by else "System"

    invited_by_email.short_description = "Invited By"

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_used:
            return False
        return super().has_change_permission(request, obj)

# LOCATIONS (READ-ONLY)
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")
    search_fields = ("name", "code")
    readonly_fields = ("name", "code")


@admin.register(RevenueDivision)
class RevenueDivisionAdmin(admin.ModelAdmin):
    list_display = (
        "division_name",
        "division_code",
        "district",
        "display_order",
    )

    search_fields = ("division_name", "division_code")
    list_filter = ("district",)

    readonly_fields = (
        "division_name",
        "division_code",
        "district",
    )


@admin.register(Mandal)
class MandalAdmin(admin.ModelAdmin):
    list_display = (
        "mandal_name",
        "mandal_code",
        "division",
        "is_municipality",
        "display_order",
    )

    search_fields = ("mandal_name", "mandal_code")
    list_filter = ("division", "is_municipality")

    readonly_fields = (
        "mandal_name",
        "mandal_code",
        "division",
    )


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = (
        "village_name",
        "village_code",
        "mandal",
        "display_order",
    )

    search_fields = ("village_name", "village_code")
    list_filter = ("mandal",)

    readonly_fields = (
        "village_name",
        "village_code",
        "mandal",
    )

# CHOICES (ENUMS)
@admin.register(ChoiceCategory)
class ChoiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(ChoiceOption)
class ChoiceOptionAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "label",
        "category",
        "display_order",
        "is_active",
    )

    list_filter = ("category", "is_active")
    search_fields = ("code", "label")
    ordering = ("category", "display_order")

# SURVEY SCHEMA (EDITABLE)
@admin.register(SurveyStep)
class SurveyStepAdmin(admin.ModelAdmin):
    list_display = (
        "step_id",
        "title",
        "step_number",
        "total_steps",
    )

    ordering = ("step_number",)


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question_id",
        "label",
        "step",
        "input_type",
        "required",
    )

    list_filter = (
        "step",
        "input_type",
        "required",
    )

    search_fields = (
        "question_id",
        "label",
    )

# SURVEY SUBMISSION (READ-ONLY)
@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "reference_id",
        "district",
        "division",
        "mandal",
        "created_at",
    )

    search_fields = ("reference_id",)
    list_filter = (
        "district",
        "division",
        "mandal",
    )

    readonly_fields = [f.name for f in SurveySubmission._meta.fields]

    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# SURVEY ANSWERS (READ-ONLY)
@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "submission",
        "question",
        "value",
    )

    search_fields = (
        "submission__reference_id",
        "question__question_id",
    )

    readonly_fields = [f.name for f in SurveyAnswer._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
