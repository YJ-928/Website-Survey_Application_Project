from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    total_responses = serializers.IntegerField()
    completed_surveys = serializers.IntegerField()

class ChartDataSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.IntegerField()
