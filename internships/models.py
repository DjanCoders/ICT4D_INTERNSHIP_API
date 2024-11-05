from django.db import models
from django.conf import settings
from accounts.models import CustomUser

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

class InternshipApplication(models.Model):
    applicant=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='application',null=True,blank=True)
    applly_for=models.ForeignKey(Internship,related_name='internship',on_delete=models.CASCADE,blank=True,null=True)
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
    resume = models.FileField(upload_to='resumes/',blank=True, null=True)
    cover_letter = models.FileField(upload_to='cover_letters/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"    

    
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
    category=models.ForeignKey(Internship,related_name='mcq_questions',on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"MCQ: {self.text}"

class DescQuestion(BaseQuestion):
    short_answer = models.CharField(max_length=255, blank=True, null=True)
    category=models.ForeignKey(Internship,related_name='desc_questions',on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return f"Descriptive: {self.text}"

class Option(models.Model):
    question = models.ForeignKey(MCQQuestion, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Answer(models.Model):
    REVIEW_STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="answers",blank=True, null=True)  
    mcq_answer = models.ForeignKey(Option, on_delete=models.CASCADE, blank=True, null=True)
    desc_answer = models.TextField(blank=True, null=True)
    mcq_question = models.ForeignKey(MCQQuestion, null=True, blank=True, on_delete=models.CASCADE)
    descriptive_question = models.ForeignKey(DescQuestion, null=True, blank=True, on_delete=models.CASCADE)
    review_status = models.CharField(max_length=10, choices=REVIEW_STATUS_CHOICES, default='PENDING')
    admin_feedback = models.TextField(blank=True, null=True)

    def is_correct(self):
        if self.mcq_question and self.mcq_answer:
            return self.mcq_answer.is_answer  # Returns True if mcq_answer is correct
        elif self.descriptive_question:
            return None  # Descriptive answers do not have automatic correctness
        return False
    
class Notification(models.Model):
    message=models.CharField(max_length=255)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  self.message   
from django.db import models

class ExamSettings(models.Model):
    category = models.OneToOneField(Internship, related_name='exam_settings', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    duration = models.IntegerField()  # Duration in minutes

    def __str__(self):
        return f"{self.category.title} - Exam starts at {self.start_time} for {self.duration} minutes"

