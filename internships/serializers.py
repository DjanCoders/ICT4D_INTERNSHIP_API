from rest_framework import serializers

from .models import Internship, Application, Question, Answer,InternshipApplication

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text']

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
    
    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers')
        instance.internship = validated_data.get('internship', instance.internship)
        instance.resume = validated_data.get('resume', instance.resume)
        instance.cover_letter = validated_data.get('cover_letter', instance.cover_letter)
        instance.status = validated_data.get('status', instance.status)
        instance.university = validated_data.get('university', instance.university)
        instance.save()

        for answer_data in answers_data:
            question_data = answer_data.pop('question')
            question, created = Question.objects.get_or_create(**question_data)
            Answer.objects.update_or_create(application=instance, question=question, defaults={'answer_text': answer_data['answer_text']})
        
        return instance
class InternshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
         model=InternshipApplication
         fields='__all__'