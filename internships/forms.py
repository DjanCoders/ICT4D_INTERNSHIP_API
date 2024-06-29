from django import forms

from .models import Internship

class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['title', 'description', 'start_date', 'end_date', 'location']