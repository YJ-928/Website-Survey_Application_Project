import random
from datetime import timedelta
from django.db import transaction
from django.utils import timezone

from api.models.survey import SurveySubmission, SurveyAnswer, SurveyQuestion
from api.models.location import District, Mandal
from api.models.choice import ChoiceCategory


TOTAL_RESPONSES = 360
MIN_MANDALS = 10
MAX_MANDALS = 15
DAYS_RANGE = 365   # 1 year for better monthly trends


def generate_submission_dates(total_count):
    """
    Generate a list of submission dates spread across the date range.
    Returns dates distributed across the year with realistic clustering.
    """
    dates = []
    now = timezone.now()
    
    # Create clusters of submissions across different time periods
    # Last 7 days: 15% of responses
    last_week_count = int(total_count * 0.15)
    for _ in range(last_week_count):
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        dates.append(now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago))
    
    # Last 30 days: 25% of responses
    last_month_count = int(total_count * 0.25)
    for _ in range(last_month_count):
        days_ago = random.randint(8, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        dates.append(now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago))
    
    # Last 90 days: 30% of responses
    last_quarter_count = int(total_count * 0.30)
    for _ in range(last_quarter_count):
        days_ago = random.randint(31, 90)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        dates.append(now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago))
    
    # Remaining responses: distributed across rest of the year
    remaining_count = total_count - len(dates)
    for _ in range(remaining_count):
        days_ago = random.randint(91, 365)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        dates.append(now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago))
    
    # Shuffle to avoid any ordering bias
    random.shuffle(dates)
    
    return dates


def seed_balanced_survey_responses(sender=None, **kwargs):
    """
    Seeds survey responses only if no survey submissions exist in the database.
    This prevents duplicate key constraint errors.
    """
    
    # Check if any survey submissions already exist
    if SurveySubmission.objects.exists():
        print("Survey responses already exist. Skipping seed_survey_responses.")
        return
    
    print("Seeding survey responses...")
    
    district = District.objects.first()
    if not district:
        print("No districts found. Please seed locations first.")
        return
    
    all_mandals = list(Mandal.objects.all())
    if not all_mandals:
        print("No mandals found. Please seed locations first.")
        return

    # Random mandal pool (avoids symmetry)
    mandals = random.sample(
        all_mandals,
        min(len(all_mandals), random.randint(MIN_MANDALS, MAX_MANDALS))
    )

    questions = {q.question_id: q for q in SurveyQuestion.objects.all()}
    choices = {
        c.code: list(c.options.values_list("code", flat=True))
        for c in ChoiceCategory.objects.prefetch_related("options")
    }

    # Create mandal-to-responses mapping for uneven distribution
    # This ensures top mandals have more villages covered
    mandal_response_counts = {}
    remaining_responses = TOTAL_RESPONSES
    
    for idx, mandal in enumerate(mandals):
        if idx < len(mandals) - 1:
            # Earlier mandals get more responses (70% concentration in first 6)
            count = max(20, int(remaining_responses / (len(mandals) - idx) * random.uniform(1.2, 1.8)))
            count = min(count, remaining_responses)
        else:
            count = remaining_responses
        mandal_response_counts[mandal] = count
        remaining_responses -= count
    
    # Generate all submission dates upfront to ensure proper distribution
    print(f"Generating {TOTAL_RESPONSES} timestamps across 365 days...")
    submission_dates = generate_submission_dates(TOTAL_RESPONSES)
    date_index = 0

    with transaction.atomic():
        response_idx = 0
        # Track used reference_ids and mobile numbers to avoid duplicates within this batch
        used_reference_ids = set()
        used_mobile_numbers = set()
        
        for mandal, response_count in mandal_response_counts.items():
            for j in range(response_count):
                response_idx += 1
                # Get all villages for this mandal and randomly select one
                villages = list(mandal.villages.all())
                village = random.choice(villages) if villages else mandal.villages.first()

                # Use pre-generated submission date
                submission_date = submission_dates[date_index]
                date_index += 1
                
                # Generate unique reference_id and mobile_number
                while True:
                    reference_id = f"REF{random.randint(100000, 999999)}"
                    if reference_id not in used_reference_ids:
                        used_reference_ids.add(reference_id)
                        break
                
                while True:
                    mobile_number = f"9{random.randint(100000000, 999999999)}"
                    if mobile_number not in used_mobile_numbers:
                        used_mobile_numbers.add(mobile_number)
                        break

                submission = SurveySubmission.objects.create(
                    reference_id=reference_id,
                    mobile_number=mobile_number,
                    district=district,
                    division=mandal.division,
                    mandal=mandal,
                    village=village,
                    created_at=submission_date,
                    is_complete=True,
            )

                employment_status = random.choice(choices["EMPLOYMENT_STATUS"])

                answers = [
                    ("AGE_GROUP", random.choice(choices["AGE_GROUP"])),
                    ("AREA_TYPE", random.choice(choices["AREA_TYPE"])),
                    ("EMPLOYMENT_STATUS", employment_status),
                ]

                # -----------------------------
                # ENTREPRENEUR / EMPLOYED
                # -----------------------------
                if employment_status in ["ENTREPRENEUR", "EMPLOYED"]:
                    answers.append(
                        ("ENTREPRENEUR_STAGE", random.choice(choices["ENTREPRENEUR_STAGE"]))
                    )

                    answers.append(
                        (
                            "INTERESTS",
                            random.sample(
                                choices["INTERESTS"],
                                random.randint(1, min(3, len(choices["INTERESTS"])))
                            )
                        )
                    )

                # -----------------------------
                # STUDENT / UNEMPLOYED
                # -----------------------------
                if employment_status in ["STUDENT", "UNEMPLOYED"]:
                    interested = random.choice(["YES", "NO"])
                    answers.append(("INTERESTED_IN_TRAINING", interested))

                    if interested == "YES":
                        answers.append(
                            (
                                "TRAINING_AREAS",
                                random.sample(
                                    choices["TRAINING_AREAS"],
                                    random.randint(1, 4)
                                )
                            )
                        )

                        answers.append(
                            ("TRAINING_MODE", random.choice(choices["TRAINING_MODE"]))
                        )

                        if random.random() > 0.4:
                            answers.append(("EMPLOYMENT_INTEREST", "YES"))
                            answers.append(
                                (
                                    "EMPLOYMENT_SECTORS",
                                    random.sample(
                                        choices["EMPLOYMENT_SECTORS"],
                                        random.randint(1, 3)
                                    )
                                )
                            )

                # -----------------------------
                # SUPPORT & LAND
                # -----------------------------
                answers.append(
                    (
                        "BASIC_SUPPORT",
                        random.sample(
                            choices["BASIC_SUPPORT"],
                            random.randint(1, len(choices["BASIC_SUPPORT"]))
                        )
                    )
                )

                answers.append(("REQUIRES_LAND", random.choice(["YES", "NO"])))
                
                # Government schemes (40% chance of availing schemes)
                availing_scheme = random.choice(["YES", "NO", "NO"])  # 33% YES, 66% NO
                answers.append(("AVAILING_GOVT_SCHEME", availing_scheme))
                
                if availing_scheme == "YES" and "GOVT_SCHEMES" in choices:
                    answers.append(
                        (
                            "GOVT_SCHEMES",
                            random.sample(
                                choices["GOVT_SCHEMES"],
                                random.randint(1, min(3, len(choices["GOVT_SCHEMES"])))
                            )
                        )
                    )
                
                # Government group membership (50% chance)
                if "GOVT_GROUP_MEMBERSHIP" in choices and random.random() > 0.5:
                    answers.append(
                        (
                            "GOVT_GROUP_MEMBERSHIP",
                            random.sample(
                                choices["GOVT_GROUP_MEMBERSHIP"],
                                random.randint(1, 2)  # 1 or 2 groups
                            )
                        )
                    )

                # -----------------------------
                # SAVE ANSWERS
                # -----------------------------
                for qid, value in answers:
                    if qid in questions:
                        SurveyAnswer.objects.create(
                            submission=submission,
                            question=questions[qid],
                            value=value
                        )
        
        print(f"Successfully seeded {TOTAL_RESPONSES} survey responses across {len(mandals)} mandals.")
