from django.contrib import admin

from .models import Internship, Application, Question

admin.site.register(Internship)
admin.site.register(Application)
admin.site.register(Question)