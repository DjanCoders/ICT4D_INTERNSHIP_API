from rest_framework import serializers

from .models import Internship, Answer,InternshipApplication, MCQQuestion, DescQuestion, Option, Answer

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_answer']

class MCQQuestionSerializer(serializers.ModelSerializer):

    options = OptionSerializer(many=True, required=False)

    class Meta:
        model = MCQQuestion
        fields = ['id', 'text', 'question_type', 'options',]

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        mcq_question = MCQQuestion.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=mcq_question, **option_data)
        return mcq_question

class DescriptiveQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = DescQuestion
        fields = ['id', 'text', 'short_answer',]

class AnswerSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.username', read_only=True)
    mcq_question_text = serializers.CharField(source='mcq_question.text', read_only=True)
    desc_question_text = serializers.CharField(source='descriptive_question.text', read_only=True)
    mcq_answer_text = serializers.CharField(source='mcq_answer.text', read_only=True)
    class Meta:
        model = Answer
        fields = [
             'id', 
            'applicant_name', 
            'mcq_question_text', 
            'desc_question_text', 
            'mcq_answer_text', 
            'desc_answer', 
            'review_status', 
            'admin_feedback'
        ]

 
class InternshipApplicationSerializer(serializers.ModelSerializer):
    internship_title = serializers.ReadOnlyField(source='applly_for.title')
    applicant_username = serializers.CharField(source='applicant.username', read_only=True)


    class Meta:
         model=InternshipApplication
         fields='__all__'
         extra_fields = ['internship_title','applicant_username']
