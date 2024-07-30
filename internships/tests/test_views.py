from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Internship, Question, Application, Answer

User = get_user_model()

class ApplyForInternshipTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        # Create an internship
        self.internship = Internship.objects.create(
            title='Software Engineer Internship', 
            description='A software engineer internship for students',
            start_date='2024-07-19',
            end_date='2024-08-19',
            location='Remote',
            is_active=True
        )

        # Create questions
        self.question1 = Question.objects.create(question_text='What is your experience with python?')
        self.question2 = Question.objects.create(question_text='Describe a project you have worked on.')

    def test_apply_for_internship(self):
        url = reverse('apply', kwargs={'pk': self.internship.id})

        data = {
            'internship': self.internship.id,
            'resume': 'test_resume.pdf',
            'cover_letter': 'This is a cover letter',
            'university': 'Test university',
            'answers': [
                {
                    'question': self.question1.id, 'answer_text': 'I have used Python for 3 years.'
                },
                {
                    'question': self.question2.id, 'answer_text': 'I have worked on a web application using Django.'
                },
            ]
        }

        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(Application.objects.get().student, self.user)