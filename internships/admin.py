from django.contrib import admin

from .models import Internship, Question,InternshipApplication

admin.site.register(Internship)
# admin.site.register(Application)
admin.site.register(Question)
admin.site.register(InternshipApplication)