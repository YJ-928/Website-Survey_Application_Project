from django.urls import path

# Auth
from api.views.admin import (
    AdminLoginView,
    AdminInviteView,
    AdminActivateView,
)

# Locations
from api.views.location import (
    DistrictListView,
    RevenueDivisionListView,
    MandalListView,
    VillageListView,
)

# Survey
from api.views.survey_schema import SurveySchemaView
from api.views.survey_submit import SubmitSurveyView
from api.views.choices import ChoiceListView

# Dashboard
from api.views.dashboard import (
    DashboardSummaryView,
    WomenStatusChartView,
    AreaTypeChartView,
    AgeDistributionChartView,
    AspirationsChartView,
    TopInterestsChartView,
    TrainingAreasTimeSeriesView,
    EntrepreneurFunnelView,
    SubmissionModeChartView,
    DistrictPriorityView,
)

# Analytics
from api.views.analytics import (
    SummaryAnalyticsView,
    QuestionAnalyticsView,
    LocationBreakdownView,
    TimeSeriesAnalyticsView,
    MultiQuestionAnalyticsView,
    AgeGroupAnalyticsView,
    MonthlyRegistrationTrendsView,
    MandalPerformanceAnalyticsView,
    GovtSchemesAnalyticsView,
    GovtGroupMembershipAnalyticsView,
)

# Internal
from api.views.encrypt_text import EncryptTestView

# Mobile
from api.views.mobile import SurveyMobileCheckView


urlpatterns = [
    # --------------------------------------------------
    # Auth (Admins only)
    # --------------------------------------------------
    path("auth/admin/login/", AdminLoginView.as_view()),
    path("auth/admin/invite/", AdminInviteView.as_view()),
    path("auth/admin/activate/", AdminActivateView.as_view()),

    # --------------------------------------------------
    # Location Masters
    # --------------------------------------------------
    path("locations/districts/", DistrictListView.as_view()),
    path("locations/divisions/", RevenueDivisionListView.as_view()),
    path("locations/mandals/", MandalListView.as_view()),
    path("locations/villages/", VillageListView.as_view()),

    # --------------------------------------------------
    # Survey (Public)
    # --------------------------------------------------
    path("survey/schema/", SurveySchemaView.as_view(), name="survey-schema"),
    path("survey/choices/", ChoiceListView.as_view(), name="survey-choices"),
    path("survey/submit/", SubmitSurveyView.as_view(), name="survey-submit"),
    path("survey/check-mobile/", SurveyMobileCheckView.as_view(), name="survey-check-mobile"),

    # --------------------------------------------------
    # Dashboard (Authenticated)
    # --------------------------------------------------
    path("dashboard/summary/", DashboardSummaryView.as_view()),
    path("dashboard/women-status/", WomenStatusChartView.as_view()),
    path("dashboard/area-type/", AreaTypeChartView.as_view()),
    path("dashboard/age-distribution/", AgeDistributionChartView.as_view()),
    path("dashboard/aspirations/", AspirationsChartView.as_view()),
    path("dashboard/top-interests/", TopInterestsChartView.as_view()),
    path("dashboard/training-areas-trends/", TrainingAreasTimeSeriesView.as_view()),
    path("dashboard/entrepreneur-funnel/", EntrepreneurFunnelView.as_view()),
    path("dashboard/submission-mode/", SubmissionModeChartView.as_view()),
    path("dashboard/district-priority/", DistrictPriorityView.as_view()),

    # --------------------------------------------------
    # Analytics (Public - Flexible aggregation APIs)
    # --------------------------------------------------
    path("analytics/summary/", SummaryAnalyticsView.as_view(), name="analytics-summary"),
    path("analytics/question/<str:question_id>/", QuestionAnalyticsView.as_view(), name="analytics-question"),
    path("analytics/location-breakdown/", LocationBreakdownView.as_view(), name="analytics-location"),
    path("analytics/time-series/", TimeSeriesAnalyticsView.as_view(), name="analytics-time-series"),
    path("analytics/age-group/", AgeGroupAnalyticsView.as_view(), name="analytics-age-group"),
    path("analytics/monthly-registration-trends/", MonthlyRegistrationTrendsView.as_view(), name="analytics-monthly-trends"),
    path("analytics/mandal-performance/", MandalPerformanceAnalyticsView.as_view(), name="analytics-mandal-performance"),
    path("analytics/govt-schemes/", GovtSchemesAnalyticsView.as_view(), name="analytics-govt-schemes"),
    path("analytics/govt-group-membership/", GovtGroupMembershipAnalyticsView.as_view(), name="analytics-govt-group-membership"),
    path("analytics/multi-question/", MultiQuestionAnalyticsView.as_view(), name="analytics-multi-question"),

    # --------------------------------------------------
    # Internal / Debug
    # --------------------------------------------------
    path("internal/encrypt-text/", EncryptTestView.as_view()),


]
