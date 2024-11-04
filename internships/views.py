from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (InternshipSerializer,
                           InternshipApplicationSerializer,
                             MCQQuestionSerializer, 
                          DescriptiveQuestionSerializer,AnswerSerializer)
from .models import( Internship, MCQQuestion, 
                    MCQQuestion,InternshipApplication,
                    Notification,DescQuestion,Answer)
from .permissions import IsAdminOrReadOnly
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime
import calendar
from rest_framework.permissions import AllowAny
from accounts.models import Profile

class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [IsAdminOrReadOnly]
class InternshipStatusUpdateView(generics.UpdateAPIView):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # Only update the status field
        instance.is_active = request.data.get("is_active", instance.is_active)
        instance.save()
        return Response({"is_active": instance.is_active}, status=status.HTTP_200_OK) 

class MCQQuestionViewSet(viewsets.ModelViewSet):
    queryset = MCQQuestion.objects.all()
    serializer_class = MCQQuestionSerializer
    permission_classes = [IsAdminOrReadOnly]

class DescriptiveQuestionViewSet(viewsets.ModelViewSet):
    queryset = DescQuestion.objects.all()
    serializer_class = DescriptiveQuestionSerializer
    permission_classes = [IsAdminOrReadOnly]


class InternshipApplicationView(viewsets.ModelViewSet):
    serializer_class = InternshipApplicationSerializer
    queryset = InternshipApplication.objects.all()
    permission_classes = [IsAuthenticated]  # Ensure only logged-in users can create applications

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        return queryset

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        apply_for_id = request.data.get('applly_for')

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not apply_for_id:
            return Response({"error": "applly_for field is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            apply_for_instance = Internship.objects.get(id=apply_for_id)
        except Internship.DoesNotExist:
            return Response({"error": "Invalid internship selection"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if an application with this email and internship already exists for this user
        user = request.user
        try:
           
            existing_application = InternshipApplication.objects.get(
                email=email, applly_for=apply_for_instance, applicant=user
            )
            serializer = self.get_serializer(existing_application, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            profile=Profile.objects.get(user=user)
            profile.is_internee=True
            profile.save()
            return Response({"message": "Application updated successfully!"}, status=status.HTTP_200_OK)
        except InternshipApplication.DoesNotExist:
            # Create a new application
            profile=Profile.objects.get(user=user)
            if not profile:
                return Response({"message": "User Profle Does not exist!"}, status=status.HTTP_404_NOT_FOUND)
            profile.is_internee=True
            profile.save()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(applicant=user)
            return Response({"message": "Application submitted successfully!"}, status=status.HTTP_201_CREATED)
class MonthlyApplicationCountView(APIView):
    
    def get(self,request):
        monthly_data = (
            InternshipApplication.objects
            .annotate(month=TruncMonth("created_at"))  
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )  
        #format the data
        result = [
            {
                "name": calendar.month_name[month_data["month"].month],  # Get month name
                "total": month_data["total"]
            }
            for month_data in monthly_data
        ] 
        return Response(result) 
    
class InternshipApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = InternshipApplication.objects.all()
    serializer_class = InternshipApplicationSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        # Only update the status field
        instance.status = request.data.get("status", instance.status)
        instance.save()
        return Response({"status": instance.status}, status=status.HTTP_200_OK)   

def get_applicant_counts(request):
    data={
        'totalApplicants': InternshipApplication.objects.count(),
        'approvedApplicants': InternshipApplication.objects.filter(status='Approved').count(),
        'pendingApplicants': InternshipApplication.objects.filter(status='Pending').count(),
        'rejectedApplicants': InternshipApplication.objects.filter(status='Rejected').count(),
    }
    return JsonResponse(data)

class UnreadNotificationsView(APIView):
    def get(self, request):
        notifications = Notification.objects.filter(is_read=False)
        data = [{"id": n.id, "message": n.message, "created_at": n.created_at} for n in notifications]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        Notification.objects.filter(is_read=False).update(is_read=True)
        return Response({"id":1,"message": "Notifications marked as read."}, status=status.HTTP_200_OK)
class GetQuestionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = []

        # Retrieve the internships the user has applied for
        applied_categories = Internship.objects.filter(
            internship__applicant=request.user
        ).distinct()

        # Loop through each category to get unanswered questions
        for category in applied_categories:
            # Get answered MCQ question IDs
            answered_mcq_ids = Answer.objects.filter(
                applicant=request.user,
                mcq_question__category=category,
                mcq_answer__isnull=False
            ).values_list('mcq_question_id', flat=True)

            # Get unanswered MCQ questions
            mcq_questions = MCQQuestion.objects.filter(
                category=category
            ).exclude(id__in=answered_mcq_ids)

            # Get answered descriptive question IDs
            answered_desc_ids = Answer.objects.filter(
                applicant=request.user,
                descriptive_question__category=category,
                desc_answer__isnull=False
            ).values_list('descriptive_question_id', flat=True)

            # Get unanswered descriptive questions
            desc_questions = DescQuestion.objects.filter(
                category=category
            ).exclude(id__in=answered_desc_ids)

            # Serialize the questions
            mcq_serializer = MCQQuestionSerializer(mcq_questions, many=True)
            desc_serializer = DescriptiveQuestionSerializer(desc_questions, many=True)
            if not mcq_serializer.data and not desc_serializer.data:
                return data

            # Add category information along with unanswered questions
            data.append({
                "category_name": category.title,
                "mcq_questions": mcq_serializer.data,
                "desc_questions": desc_serializer.data,
            })

        return Response(data)

       


      
        
class SubmitAnswersAPIView(APIView):
    def post(self, request):
        answers_data = request.data
        user=request.user
        # Iterate through each answer submitted
        for answer_data in answers_data:
            mcq_question_id = answer_data.get('mcq_question')
            descriptive_question_id = answer_data.get('descriptive_question')

            # Check if an answer already exists for the given questions
            existing_answer = Answer.objects.filter(
                mcq_question__id=mcq_question_id,
                descriptive_question__id=descriptive_question_id,
                applicant=user
            ).first()
            
            # Prepare the answer data
            if existing_answer:
                # Update existing answer
                existing_answer.mcq_answer_id = answer_data.get('mcq_answer')
                existing_answer.desc_answer = answer_data.get('desc_answer')
                existing_answer.save()
            else:
                # Create a new answer
                serializer = AnswerSerializer(data=answer_data)
                if serializer.is_valid():

                   serializer.save(applicant=user)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Answers submitted successfully!"}, status=status.HTTP_201_CREATED)
class AnswerListView(APIView):
    permission_classes = [IsAdminOrReadOnly]  # Restrict access to admin users

    def get(self, request):
        # Fetch all answers, including related applicant, question, and options if available
        answers = Answer.objects.select_related('applicant', 'mcq_question', 'descriptive_question', 'mcq_answer').all()
        
        # Serialize the data to send as JSON
        serializer = AnswerSerializer(answers, many=True)
        
        return Response(serializer.data)
    def patch(self, request, pk):
        try:
            # Retrieve the answer by primary key
            answer = Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            return Response({'error': 'Answer not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the request data contains the review status
        status_data = request.data.get('review_status', None)
        if status_data:
            answer.review_status = status_data  # Update the review status

        # Optionally, you can include admin feedback if provided
        feedback_data = request.data.get('admin_feedback', None)
        if feedback_data:
            answer.admin_feedback = feedback_data  # Update admin feedback
        
        # Save the updated answer
        answer.save()

        # Serialize the updated answer
        serializer = AnswerSerializer(answer)

        return Response(serializer.data, status=status.HTTP_200_OK)