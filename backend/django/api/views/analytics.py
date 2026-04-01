"""
Analytics Views - Survey Data Aggregation APIs
Optimized for dashboard charts with DB-level aggregation
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from api.models.survey import SurveySubmission, SurveyAnswer, SurveyQuestion
from api.models.location import District, RevenueDivision, Mandal


class SummaryAnalyticsView(APIView):
    """
    GET /api/analytics/summary/
    Returns overall summary statistics
    """
    
    def get(self, request):
        try:
            total_responses = SurveySubmission.objects.count()
            
            # Get unique districts, divisions, mandals, villages
            districts = SurveySubmission.objects.values('district__name').distinct().count()
            divisions = SurveySubmission.objects.values('division__division_name').distinct().count()
            mandals = SurveySubmission.objects.values('mandal__mandal_name').distinct().count()
            villages = SurveySubmission.objects.values('village__village_name').distinct().count()
            
            # Most active district
            top_district = SurveySubmission.objects.values('district__name')\
                .annotate(count=Count('submission_id'))\
                .order_by('-count')\
                .first()
            
            return Response({
                'total_responses': total_responses,
                'districts_covered': districts,
                'divisions_covered': divisions,
                'mandals_covered': mandals,
                'villages_covered': villages,
                'top_district': top_district['district__name'] if top_district else None,
                'top_district_count': top_district['count'] if top_district else 0
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QuestionAnalyticsView(APIView):
    """
    GET /api/analytics/question/<question_id>/
    Returns aggregated data for a specific question
    Supports radio, checkbox, dropdown, chips, cards
    """
    
    def get(self, request, question_id):
        try:
            # Get the question
            question = SurveyQuestion.objects.filter(question_id=question_id).first()
            if not question:
                return Response(
                    {'error': 'Question not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get all answers for this question
            answers = SurveyAnswer.objects.filter(
                question__question_id=question_id
            ).values_list('value', flat=True)
            
            # Aggregate based on input type
            if question.input_type in ['radio', 'dropdown', 'cards']:
                # Single value answers
                aggregated = {}
                for value in answers:
                    if isinstance(value, str):
                        aggregated[value] = aggregated.get(value, 0) + 1
            
            elif question.input_type in ['checkbox', 'chips']:
                # Multi-value answers
                aggregated = {}
                for value in answers:
                    if isinstance(value, list):
                        for item in value:
                            aggregated[item] = aggregated.get(item, 0) + 1
            
            else:
                aggregated = {}
            
            # Convert to chart format
            labels = list(aggregated.keys())
            values = list(aggregated.values())
            
            return Response({
                'question_id': question_id,
                'question_label': question.label,
                'input_type': question.input_type,
                'total_responses': len(answers),
                'labels': labels,
                'values': values,
                'data': aggregated
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LocationBreakdownView(APIView):
    """
    GET /api/analytics/location-breakdown/
    Query params: ?level=district|division|mandal
    Returns submission counts by location
    """
    
    def get(self, request):
        try:
            level = request.query_params.get('level', 'district')
            
            if level == 'district':
                data = SurveySubmission.objects.values('district__name')\
                    .annotate(count=Count('submission_id'))\
                    .order_by('-count')
                label_key = 'district__name'
                
            elif level == 'division':
                data = SurveySubmission.objects.values('division__division_name')\
                    .annotate(count=Count('submission_id'))\
                    .order_by('-count')
                label_key = 'division__division_name'
                
            elif level == 'mandal':
                data = SurveySubmission.objects.values('mandal__mandal_name')\
                    .annotate(count=Count('submission_id'))\
                    .order_by('-count')
                label_key = 'mandal__mandal_name'
            else:
                return Response(
                    {'error': 'Invalid level parameter'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            labels = [item[label_key] for item in data]
            values = [item['count'] for item in data]
            
            return Response({
                'level': level,
                'labels': labels,
                'values': values
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TimeSeriesAnalyticsView(APIView):
    """
    GET /api/analytics/time-series/
    Query params: ?period=daily|weekly|monthly
    Returns submission trends over time
    """
    
    def get(self, request):
        try:
            from django.utils import timezone
            from datetime import timedelta
            
            period = request.query_params.get('period', 'daily')
            
            if period == 'daily':
                # Last 30 days
                end_date = timezone.now()
                start_date = end_date - timedelta(days=30)
                
                data = SurveySubmission.objects.filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date
                ).annotate(
                    date=TruncDate('created_at')
                ).values('date').annotate(
                    count=Count('submission_id')
                ).order_by('date')
                
            elif period == 'weekly':
                # Last 12 weeks
                end_date = timezone.now()
                start_date = end_date - timedelta(weeks=12)
                
                data = SurveySubmission.objects.filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date
                ).annotate(
                    date=TruncDate('created_at')
                ).values('date').annotate(
                    count=Count('submission_id')
                ).order_by('date')
                
            elif period == 'monthly':
                # Last 12 months
                end_date = timezone.now()
                start_date = end_date - timedelta(days=365)
                
                data = SurveySubmission.objects.filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date
                ).annotate(
                    date=TruncDate('created_at')
                ).values('date').annotate(
                    count=Count('submission_id')
                ).order_by('date')
            else:
                return Response(
                    {'error': 'Invalid period parameter'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            labels = [item['date'].strftime('%Y-%m-%d') for item in data]
            values = [item['count'] for item in data]
            
            return Response({
                'period': period,
                'labels': labels,
                'values': values
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MultiQuestionAnalyticsView(APIView):
    """
    POST /api/analytics/multi-question/
    Body: {"question_ids": ["q1", "q2", "q3"]}
    Returns aggregated data for multiple questions at once
    """
    
    def post(self, request):
        try:
            question_ids = request.data.get('question_ids', [])
            
            if not question_ids:
                return Response(
                    {'error': 'question_ids array is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            results = {}
            
            for question_id in question_ids:
                question = SurveyQuestion.objects.filter(question_id=question_id).first()
                if not question:
                    continue
                
                answers = SurveyAnswer.objects.filter(
                    question__question_id=question_id
                ).values_list('value', flat=True)
                
                # Aggregate based on input type
                if question.input_type in ['radio', 'dropdown', 'cards']:
                    aggregated = {}
                    for value in answers:
                        if isinstance(value, str):
                            aggregated[value] = aggregated.get(value, 0) + 1
                
                elif question.input_type in ['checkbox', 'chips']:
                    aggregated = {}
                    for value in answers:
                        if isinstance(value, list):
                            for item in value:
                                aggregated[item] = aggregated.get(item, 0) + 1
                else:
                    aggregated = {}
                
                results[question_id] = {
                    'question_label': question.label,
                    'input_type': question.input_type,
                    'labels': list(aggregated.keys()),
                    'values': list(aggregated.values()),
                    'data': aggregated
                }
            
            return Response(results)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AgeGroupAnalyticsView(APIView):
    """
    GET /api/analytics/age-group/
    Returns aggregated data for age group distribution
    """
    
    def get(self, request):
        try:
            from api.models.choice import ChoiceCategory
            
            # Get the AGE_GROUP question
            question = SurveyQuestion.objects.filter(question_id='AGE_GROUP').first()
            if not question:
                return Response({
                    'question_id': 'AGE_GROUP',
                    'question_label': 'Age Group',
                    'input_type': 'dropdown',
                    'labels': [],
                    'values': []
                })
            
            # Get choice options for mapping codes to labels
            choice_category = ChoiceCategory.objects.filter(code='AGE_GROUP').first()
            code_to_label = {}
            if choice_category:
                code_to_label = {
                    option.code: option.label 
                    for option in choice_category.options.all()
                }
            
            # Get all answers for this question
            answers = SurveyAnswer.objects.filter(
                question__question_id='AGE_GROUP'
            ).values_list('value', flat=True)
            
            # Aggregate age group values and map codes to labels
            aggregated = {}
            for value in answers:
                if isinstance(value, str):
                    # Use label if available, otherwise use code
                    display_label = code_to_label.get(value, value)
                    aggregated[display_label] = aggregated.get(display_label, 0) + 1
            
            # Convert to chart format, maintaining order
            labels = list(aggregated.keys())
            values = list(aggregated.values())
            
            return Response({
                'question_id': 'AGE_GROUP',
                'question_label': 'Age Group',
                'input_type': 'dropdown',
                'total_responses': len(answers),
                'labels': labels,
                'values': values,
                'data': aggregated
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MonthlyRegistrationTrendsView(APIView):
    """
    GET /api/analytics/monthly-registration-trends/
    Returns monthly submission trends for last 12 months
    """
    
    def get(self, request):
        try:
            from django.db.models.functions import TruncMonth
            from django.utils import timezone
            from datetime import timedelta
            import calendar
            
            # Get last 12 months of data
            end_date = timezone.now()
            start_date = end_date - timedelta(days=365)
            
            data = SurveySubmission.objects.filter(
                created_at__gte=start_date,
                created_at__lte=end_date
            ).annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(
                count=Count('submission_id')
            ).order_by('month')
            
            if not data:
                return Response({
                    'period': 'monthly',
                    'labels': [],
                    'values': []
                })
            
            # Format the data
            formatted_data = []
            for item in data:
                if item['month']:
                    month_name = item['month'].strftime('%b')  # Get 'Jan', 'Feb', etc.
                    formatted_data.append({
                        'month': month_name,
                        'date': item['month'].strftime('%Y-%m-%d'),
                        'count': item['count']
                    })
            
            labels = [item['month'] for item in formatted_data]
            values = [item['count'] for item in formatted_data]
            
            return Response({
                'period': 'monthly',
                'labels': labels,
                'values': values
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MandalPerformanceAnalyticsView(APIView):
    """
    GET /api/analytics/mandal-performance/
    Returns mandal performance data for polar chart (top mandals with submission counts)
    """
    
    def get(self, request):
        try:
            from django.db.models import Count
            
            # Get unique villages per mandal and count submissions
            mandal_data = SurveySubmission.objects.values('mandal__mandal_name', 'mandal__id')\
                .annotate(
                    submission_count=Count('submission_id'),
                    village_count=Count('village__id', distinct=True)
                )\
                .order_by('-village_count')[:6]
            
            if not mandal_data:
                return Response({
                    'labels': [],
                    'values': [],
                    'data': []
                })
            
            # Use village count as the main metric for visualization
            labels = [item['mandal__mandal_name'] for item in mandal_data]
            values = [item['village_count'] for item in mandal_data]
            
            return Response({
                'labels': labels,
                'values': values,
                'data': [
                    {
                        'mandal': item['mandal__mandal_name'],
                        'villages_covered': item['village_count'],
                        'total_submissions': item['submission_count']
                    }
                    for item in mandal_data
                ]
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GovtSchemesAnalyticsView(APIView):
    """
    GET /api/analytics/govt-schemes/
    Returns aggregated data for government schemes availed
    Maps scheme codes to labels
    """
    
    def get(self, request):
        try:
            from api.models.choice import ChoiceCategory
            
            # Get the GOVT_SCHEMES question
            question = SurveyQuestion.objects.filter(question_id='GOVT_SCHEMES').first()
            if not question:
                return Response({
                    'question_id': 'GOVT_SCHEMES',
                    'question_label': 'Government Schemes Availed',
                    'input_type': 'checkbox',
                    'labels': [],
                    'values': [],
                    'data': {}
                })
            
            # Get choice options for mapping codes to labels
            choice_category = ChoiceCategory.objects.filter(code='GOVT_SCHEMES').first()
            code_to_label = {}
            if choice_category:
                code_to_label = {
                    option.code: option.label 
                    for option in choice_category.options.all()
                }
            
            # Get all answers for this question (multi-select checkbox)
            answers = SurveyAnswer.objects.filter(
                question__question_id='GOVT_SCHEMES'
            ).values_list('value', flat=True)
            
            # Aggregate scheme values and map codes to labels
            aggregated = {}
            for value in answers:
                if isinstance(value, list):
                    # Multi-select: iterate through each selected scheme
                    for item in value:
                        display_label = code_to_label.get(item, item)
                        aggregated[display_label] = aggregated.get(display_label, 0) + 1
            
            # Sort by frequency descending for better UX
            sorted_items = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
            labels = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]
            aggregated = dict(sorted_items)
            
            return Response({
                'question_id': 'GOVT_SCHEMES',
                'question_label': 'Government Schemes Availed',
                'input_type': 'checkbox',
                'total_responses': len(answers),
                'labels': labels,
                'values': values,
                'data': aggregated
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GovtGroupMembershipAnalyticsView(APIView):
    """
    GET /api/analytics/govt-group-membership/
    Returns aggregated data for government group membership
    Maps membership codes to labels
    """
    
    def get(self, request):
        try:
            from api.models.choice import ChoiceCategory
            
            # Get the GOVT_GROUP_MEMBERSHIP question
            question = SurveyQuestion.objects.filter(question_id='GOVT_GROUP_MEMBERSHIP').first()
            if not question:
                return Response({
                    'question_id': 'GOVT_GROUP_MEMBERSHIP',
                    'question_label': 'Government Group Membership',
                    'input_type': 'checkbox',
                    'labels': [],
                    'values': [],
                    'data': {}
                })
            
            # Get choice options for mapping codes to labels
            choice_category = ChoiceCategory.objects.filter(code='GOVT_GROUP_MEMBERSHIP').first()
            code_to_label = {}
            if choice_category:
                code_to_label = {
                    option.code: option.label 
                    for option in choice_category.options.all()
                }
            
            # Get all answers for this question (multi-select checkbox)
            answers = SurveyAnswer.objects.filter(
                question__question_id='GOVT_GROUP_MEMBERSHIP'
            ).values_list('value', flat=True)
            
            # Aggregate membership values and map codes to labels
            aggregated = {}
            for value in answers:
                if isinstance(value, list):
                    # Multi-select: iterate through each selected membership
                    for item in value:
                        display_label = code_to_label.get(item, item)
                        aggregated[display_label] = aggregated.get(display_label, 0) + 1
            
            # Sort by frequency descending for better UX
            sorted_items = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)
            labels = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]
            aggregated = dict(sorted_items)
            
            return Response({
                'question_id': 'GOVT_GROUP_MEMBERSHIP',
                'question_label': 'Government Group Membership',
                'input_type': 'checkbox',
                'total_responses': len(answers),
                'labels': labels,
                'values': values,
                'data': aggregated
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
