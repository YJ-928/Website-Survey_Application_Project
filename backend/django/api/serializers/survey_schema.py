from rest_framework import serializers
from api.models.survey import SurveyStep, SurveyQuestion
from api.serializers.choice import ChoiceOptionSerializer
from api.utils.translate import translate


class SurveyQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    class Meta:
        model = SurveyQuestion
        fields = (
            "question_id",
            "label",
            "input_type",
            "required",
            "visible_when",
            "options",
        )
    
    def get_label(self, obj):
        """Translate label based on language in context"""
        language = self.context.get('language', 'en')
        return translate(obj.label, language)

    def get_options(self, obj):
        if not obj.options_category:
            return []
        language = self.context.get('language', 'en')
        return ChoiceOptionSerializer(
            obj.options_category.options.filter(is_active=True),
            many=True,
            context={'language': language}
        ).data


class SurveyStepSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = SurveyStep
        fields = (
            "step_id",
            "title",
            "step_number",
            "total_steps",
            "questions",
        )
    
    def get_title(self, obj):
        """Translate title based on language in context"""
        language = self.context.get('language', 'en')
        return translate(obj.title, language)
    
    def get_questions(self, obj):
        """Get questions and pass language context"""
        language = self.context.get('language', 'en')
        return SurveyQuestionSerializer(obj.questions, many=True, context={'language': language}).data
