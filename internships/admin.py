from django.contrib import admin

from .models import Internship, InternshipApplication, MCQQuestion, DescQuestion, Option, Answer,Notification
admin.site.register(Notification)
admin.site.register(Internship)
class InternshipApplicationAdmin(admin.ModelAdmin):
    model=InternshipApplication
    list_display=['first_name','last_name','email','applly_for']
class OptionInline(admin.TabularInline):
    model = Option
    extra = 1  # Number of empty forms to display

class MCQQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type')
    inlines = [OptionInline]

class DescriptiveQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'short_answer')

class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'applicant', 
        'get_mcq_question_text', 
        'get_desc_question_text', 
        'get_mcq_answer_text', 
        'desc_answer', 
        'review_status', 
        'admin_feedback'
    )

    search_fields = ('desc_answer',)

    def get_mcq_question_text(self, obj):
        return obj.mcq_question.text if obj.mcq_question else None
    get_mcq_question_text.short_description = 'MCQ Question Text'

    def get_desc_question_text(self, obj):
        return obj.descriptive_question.text if obj.descriptive_question else None
    get_desc_question_text.short_description = 'Descriptive Question Text'

    def get_mcq_answer_text(self, obj):
        return obj.mcq_answer.text if obj.mcq_answer else None
    get_mcq_answer_text.short_description = 'MCQ Answer Text'

admin.site.register(MCQQuestion, MCQQuestionAdmin)
admin.site.register(DescQuestion, DescriptiveQuestionAdmin)
admin.site.register(Option)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(InternshipApplication,InternshipApplicationAdmin)

