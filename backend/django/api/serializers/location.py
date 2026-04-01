from rest_framework import serializers

from api.models.location import District, Mandal, RevenueDivision, Village
from api.utils.translate import translate


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for validating district"""
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = District
        fields = ("id", "name", "code")
    
    def get_name(self, obj):
        """Translate district name based on language in context"""
        language = self.context.get('language', 'en')
        return translate(obj.name, language)


class RevenueDivisionSerializer(serializers.ModelSerializer):
    """Serializer for validating revenue-division"""
    division_name = serializers.SerializerMethodField()
    
    class Meta:
        model = RevenueDivision
        fields = (
            "id",
            "division_code",
            "division_name",
        )
    
    def get_division_name(self, obj):
        """Translate division name based on language in context"""
        language = self.context.get('language', 'en')
        return translate(obj.division_name, language)


class MandalSerializer(serializers.ModelSerializer):
    """Serializer for validating mandal"""
    mandal_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Mandal
        fields = (
            "id",
            "mandal_code",
            "mandal_name",
            "local_name",
            "is_municipality",
        )
    
    def get_mandal_name(self, obj):
        """Translate mandal name based on language in context"""
        language = self.context.get('language', 'en')
        # First try local_name if Telugu and available
        if language == 'te' and obj.local_name:
            return obj.local_name
        # Otherwise use translate function
        return translate(obj.mandal_name, language)


class VillageSerializer(serializers.ModelSerializer):
    """Serializer for validating village"""
    village_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Village
        fields = (
            "id",
            "village_code",
            "village_name",
            "local_name",
        )
    
    def get_village_name(self, obj):
        """Translate village name based on language in context"""
        language = self.context.get('language', 'en')
        # First try local_name if Telugu and available
        if language == 'te' and obj.local_name:
            return obj.local_name
        # Otherwise use translate function
        return translate(obj.village_name, language)
