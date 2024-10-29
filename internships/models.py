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

    
class BaseQuestion(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice Question'),
        ('DESC', 'Descriptive Question'),
    ]

    text = models.TextField()
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPES)

    class Meta:
        abstract = True

class MCQQuestion(BaseQuestion):
    def __str__(self):
        return f"MCQ: {self.text}"

class DescQuestion(BaseQuestion):
    short_answer = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Descriptive: {self.text}"

class Option(models.Model):
    question = models.ForeignKey(MCQQuestion, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Answer(models.Model):
    mcq_answer = models.ForeignKey(Option, on_delete=models.CASCADE, blank=True, null=True)
    desc_answer = models.TextField(blank=True, null=True)
    mcq_question = models.ForeignKey(MCQQuestion, null=True, blank=True, on_delete=models.CASCADE)
    descriptive_question = models.ForeignKey(DescQuestion, null=True, blank=True, on_delete=models.CASCADE)

    REVIEW_STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    review_status = models.CharField(max_length=10, choices=REVIEW_STATUS_CHOICES, default='PENDING')
    admin_feedback = models.TextField(blank=True, null=True)

    def is_correct(self):
        if isinstance(self.question, MCQQuestion) and self.mcq_answer:
            return self.mcq_answer.is_answer
        elif isinstance(self.question, DescQuestion):
            # Skip automatic correctness check; to be reviewed by admin
            return None  
        return False