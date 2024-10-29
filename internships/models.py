from django.db import models
from django.conf import settings

class Internship(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
from django.db import models

class InternshipApplication(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    start_date = models.DateField()
    duration = models.IntegerField()  # Duration in months
    department = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/',blank=True, null=True)
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.department}"    



class Application(models.Model):
    intern = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.FileField(upload_to='cover_letter/')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    university = models.CharField(max_length=100)

    def __str__(self):
        return f'Application by {self.intern.username} for {self.internship}'
    

class Question(models.Model):
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f'{self.question} - {self.answer_text}'