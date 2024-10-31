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
        fields = ['id', 'text', 'question_type', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options', [])
        mcq_question = MCQQuestion.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=mcq_question, **option_data)
        return mcq_question

class DescriptiveQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescQuestion
        fields = ['id', 'text', 'short_answer']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'mcq_answer', 'desc_answer', 'mcq_question', 'descriptive_question']

# # class ApplicationSerializer(serializers.ModelSerializer):
#     answers = AnswerSerializer(many=True)

#     class Meta:
#         model = Application
#         fields = '__all__'
    
#     def create(self, validated_data):
#         answers_data = self.validated_data.pop('answers')
#         application = Application.objects.create(**validated_data)
        
#         for answer_data in answers_data:
#             question_data = answer_data.pop('question')
#             question, created = Question.objects.get_or_create(**question_data)
#             Answer.objects.create(question=question, application=application, **answer_data)
        
#         return application
    
#     def update(self, instance, validated_data):
#         answers_data = validated_data.pop('answers')
#         instance.internship = validated_data.get('internship', instance.internship)
#         instance.resume = validated_data.get('resume', instance.resume)
#         instance.cover_letter = validated_data.get('cover_letter', instance.cover_letter)
#         instance.status = validated_data.get('status', instance.status)
#         instance.university = validated_data.get('university', instance.university)
#         instance.save()

#         for answer_data in answers_data:
#             question_data = answer_data.pop('question')
#             question, created = Question.objects.get_or_create(**question_data)
#             Answer.objects.update_or_create(application=instance, question=question, defaults={'answer_text': answer_data['answer_text']})
        
#         return instance
class InternshipApplicationSerializer(serializers.ModelSerializer):
    internship_title = serializers.ReadOnlyField(source='applly_for.title')

    class Meta:
         model=InternshipApplication
         fields='__all__'
         extra_fields = ['internship_title']
