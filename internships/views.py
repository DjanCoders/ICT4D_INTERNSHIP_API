from django.shortcuts import render, redirect

from .models import Internship
from .forms import InternshipForm

def index(request):
    return render(request, 'internships/index.html')

def create_internship(request):
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            # Handle form validation errors
            errors = form.errors.as_data()
            error_messages = [error[0].message for error in errors.values()]
            return render(request, 'internships/create_internships.html', {'form': form, 'error_messages': error_messages})
            
        return redirect('index')
    else:
        # Render the create internship form
        form = InternshipForm()
        return render(request, 'internships/create_internships.html', {'form': form})