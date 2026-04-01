import uuid
from django.db import models
from .location import District, RevenueDivision, Mandal, Village
from .choice import ChoiceCategory


class SurveyStep(models.Model):
    step_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    step_number = models.IntegerField()
    total_steps = models.IntegerField()

    def __str__(self):
        return self.step_id


class SurveyQuestion(models.Model):
    step = models.ForeignKey(
        SurveyStep,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_id = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=255)

    input_type = models.CharField(
        max_length=30,
        choices=[
            ("dropdown", "Dropdown"),
            ("radio", "Radio"),
            ("checkbox", "Checkbox"),
            ("chips", "Chips"),
            ("cards", "Cards"),
        ],
    )

    required = models.BooleanField(default=False)

    options_category = models.ForeignKey(
        ChoiceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    visible_when = models.JSONField(null=True, blank=True)
    order = models.IntegerField(default=0, help_text="Display order within the step")

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.question_id


class SurveySubmission(models.Model):
    submission_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    reference_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True
    )

    # Mobile number - required for unique user identification
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        db_index=True,
        help_text="10-digit mobile number of the respondent"
    )

    district = models.ForeignKey(District, on_delete=models.PROTECT)
    division = models.ForeignKey(RevenueDivision, on_delete=models.PROTECT)
    mandal = models.ForeignKey(Mandal, on_delete=models.PROTECT)
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)

    is_complete = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Survey Submission'
        verbose_name_plural = 'Survey Submissions'
        indexes = [
            models.Index(fields=['mobile_number', 'created_at']),
        ]

    def __str__(self):
        return self.reference_id


class SurveyAnswer(models.Model):
    submission = models.ForeignKey(
        SurveySubmission,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        SurveyQuestion,
        on_delete=models.CASCADE
    )

    value = models.JSONField()

    def __str__(self):
        return f"{self.question.question_id}"
