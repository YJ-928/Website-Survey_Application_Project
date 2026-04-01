import uuid
import logging
from django.db import IntegrityError, transaction
from rest_framework import serializers

from api.models.survey import (
    SurveySubmission,
    SurveyAnswer,
    SurveyQuestion,
)
from api.models.location import Mandal, RevenueDivision, Village


logger = logging.getLogger(__name__)


class SurveyAnswerInputSerializer(serializers.Serializer):
    question_id = serializers.CharField()
    value = serializers.JSONField()


class SurveySubmissionCreateSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15, required=True)
    district = serializers.IntegerField()
    division = serializers.IntegerField()
    mandal = serializers.IntegerField()
    village = serializers.IntegerField()
    answers = SurveyAnswerInputSerializer(many=True)

    def validate_mobile_number(self, value):
        """Validate mobile number format with Indian-specific rules"""
        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "Mobile number must contain only digits"
            )

        if len(value) != 10:
            raise serializers.ValidationError(
                "Mobile number must be 10 digits"
            )

        # Indian mobile numbers start with 6, 7, 8, or 9
        if value[0] not in ['6', '7', '8', '9']:
            raise serializers.ValidationError(
                "Invalid mobile number format"
            )

        # Prevent obvious fake numbers
        if len(set(value)) == 1:
            raise serializers.ValidationError(
                "Invalid mobile number"
            )

        return value

    def validate(self, data):
        # Validate location hierarchy in a single optimized query
        try:
            village = Village.objects.select_related(
                'mandal__division__district'
            ).get(id=data["village"])
        except Village.DoesNotExist:
            raise serializers.ValidationError("Invalid village")

        if village.mandal_id != data["mandal"]:
            raise serializers.ValidationError(
                "Invalid village for given mandal"
            )

        if village.mandal.division_id != data["division"]:
            raise serializers.ValidationError(
                "Invalid mandal for given division"
            )

        if village.mandal.division.district_id != data["district"]:
            raise serializers.ValidationError(
                "Invalid division for given district"
            )

        question_ids = [a["question_id"] for a in data["answers"]]

        # Fetch ALL questions once with related data (optimization)
        all_questions = SurveyQuestion.objects.select_related(
            "options_category"
        ).prefetch_related("options_category__options")

        all_question_map = {q.question_id: q for q in all_questions}

        # Validate that all submitted question IDs exist
        for qid in question_ids:
            if qid not in all_question_map:
                raise serializers.ValidationError(
                    f"Invalid question_id: {qid}"
                )

        # Build answer lookup
        answer_map = {
            a["question_id"]: a["value"]
            for a in data["answers"]
        }

        # Check for missing required questions
        missing_required = []

        for q in all_question_map.values():
            if not q.required:
                continue

            # Check if question is visible based on dependencies
            if q.visible_when:
                visible = True
                for dep_qid, dep_values in q.visible_when.items():
                    if answer_map.get(dep_qid) not in dep_values:
                        visible = False
                        break
                if not visible:
                    continue

            if q.question_id not in answer_map:
                missing_required.append(q.question_id)

        if missing_required:
            raise serializers.ValidationError(
                f"Missing required questions: {', '.join(missing_required)}"
            )

        # Validate option values - optimized with pre-cached allowed options
        # Build a cache of allowed options for each question to avoid repeated queries
        options_cache = {}
        for q in all_question_map.values():
            if q.options_category:
                options_cache[q.question_id] = set(
                    q.options_category.options
                    .filter(is_active=True)
                    .values_list("code", flat=True)
                )

        # Now validate each answer using the cache
        for ans in data["answers"]:
            q = all_question_map[ans["question_id"]]

            if q.question_id in options_cache:
                allowed = options_cache[q.question_id]
                val = ans["value"]

                if isinstance(val, list):
                    if not set(val).issubset(allowed):
                        raise serializers.ValidationError(
                            f"Invalid option in {q.question_id}"
                        )
                else:
                    if val not in allowed:
                        raise serializers.ValidationError(
                            f"Invalid option in {q.question_id}"
                        )

        data["question_map"] = all_question_map
        return data

    def create(self, validated_data):
        reference_id = f"WE-{uuid.uuid4().hex[:6].upper()}"
        question_map = validated_data.pop("question_map")
        mobile_number = validated_data["mobile_number"]

        # Log submission attempt (mask last 6 digits for privacy)
        masked_mobile = mobile_number[:4] + "******" if len(mobile_number) == 10 else "******"
        logger.info(
            f"Survey submission attempt: mobile={masked_mobile}, "
            f"district={validated_data['district']}, "
            f"village={validated_data['village']}, "
            f"num_answers={len(validated_data['answers'])}"
        )

        # Use atomic transaction to prevent partial data and database locks
        try:
            with transaction.atomic():
                submission = SurveySubmission.objects.create(
                    reference_id=reference_id,
                    mobile_number=mobile_number,
                    district_id=validated_data["district"],
                    division_id=validated_data["division"],
                    mandal_id=validated_data["mandal"],
                    village_id=validated_data["village"],
                )

                SurveyAnswer.objects.bulk_create(
                    SurveyAnswer(
                        submission=submission,
                        question=question_map[a["question_id"]],
                        value=a["value"],
                    )
                    for a in validated_data["answers"]
                )

                logger.info(
                    f"Survey submitted successfully: reference_id={reference_id}, "
                    f"mobile={masked_mobile}"
                )

        except IntegrityError as e:
            error_msg = str(e).lower()
            logger.warning(
                f"Survey submission failed - IntegrityError: mobile={masked_mobile}, "
                f"error={error_msg[:100]}"
            )
            if "mobile_number" in error_msg or "unique" in error_msg:
                raise serializers.ValidationError(
                    {"mobile_number": "This mobile number has already submitted the survey"}
                )
            raise serializers.ValidationError(
                "Failed to create submission. Please try again."
            )

        return submission


class SurveySubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveySubmission
        fields = ("reference_id", "created_at")
