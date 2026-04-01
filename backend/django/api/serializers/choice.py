from rest_framework import serializers
from api.models.choice import ChoiceCategory, ChoiceOption
from api.utils.translate import translate


class ChoiceOptionSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    
    class Meta:
        model = ChoiceOption
        fields = ("code", "label", "icon")
    
    def get_label(self, obj):
        """Translate label based on language in context"""
        language = self.context.get('language', 'en')
        return translate(obj.label, language)


class ChoiceCategorySerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = ChoiceCategory
        fields = ("code", "name", "options")
    
    def get_name(self, obj):
        """Translate name based on language in context"""
        language = self.context.get('language', 'en')
        return translate(obj.name, language)

    def get_options(self, obj):
        qs = obj.options.filter(is_active=True).order_by("display_order")
        language = self.context.get('language', 'en')
        return ChoiceOptionSerializer(qs, many=True, context={'language': language}).data
