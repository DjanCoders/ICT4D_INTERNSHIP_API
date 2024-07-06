from rest_framework import serializers

from .models import Internship, Application, Question, Answer

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()

    class Meta:
        model = Answer
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Application
        fields = '__all__'
    
    def create(self, validated_data):
        answers_data = self.validated_data.pop('answers')
        application = Application.objects.create(**validated_data)
        
        for answer_data in answers_data:
            question_data = answer_data.pop('question')
            question, created = Question.objects.get_or_create(**question_data)
            Answer.objects.create(question=question, application=application, **answer_data)
        
        return application