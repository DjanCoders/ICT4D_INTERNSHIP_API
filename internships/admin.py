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
    list_display = ('mcq_answer', 'desc_answer', 'mcq_question', 'descriptive_question','applicant')
    search_fields = ('desc_answer',)

admin.site.register(MCQQuestion, MCQQuestionAdmin)
admin.site.register(DescQuestion, DescriptiveQuestionAdmin)
admin.site.register(Option)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(InternshipApplication,InternshipApplicationAdmin)

