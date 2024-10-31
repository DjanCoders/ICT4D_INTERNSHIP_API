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

class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    # permission_classes = [IsAdminOrReadOnly]
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


   def get_queryset(self):
        queryset = super().get_queryset()

        status_parm = self.request.query_params.get('status', None)
        
        # Filter by status if the status parameter is provided
        if status_parm:
            queryset = queryset.filter(status=status_parm)
        
        return queryset
   def create(self, request, *args, **kwargs):
        email = request.data.get('email')  # Extract the email from the request data
        apply_for_id = request.data.get('applly_for')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not apply_for_id:
           return Response({"error": "applly_for field is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            apply_for_instance=Internship.objects.get(id=apply_for_id)
        except Internship.DoesNotExist:
            Response({"error": "Invalid internship selection"}, status=status.HTTP_400_BAD_REQUEST)   
        # Check if an application with this email already exists
        try:
            existing_application = InternshipApplication.objects.get(email=email, applly_for=apply_for_instance)
            serializer = self.get_serializer(existing_application, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Update the existing application
            return Response({"message": "Application updated successfully!"}, status=status.HTTP_200_OK)
        except InternshipApplication.DoesNotExist:
            # If no application exists with this email, create a new one
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Create a new application
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
    def get(self, request):
        mcq_questions = MCQQuestion.objects.all()
        desc_questions = DescQuestion.objects.all()

        mcq_serializer = MCQQuestionSerializer(mcq_questions, many=True)
        desc_serializer = DescriptiveQuestionSerializer(desc_questions, many=True)
       


        return Response({
            "mcq_questions": mcq_serializer.data,
            "desc_questions": desc_serializer.data,
        }, status=status.HTTP_200_OK)
        
class SubmitAnswersAPIView(APIView):
    def post(self, request):
        answers_data = request.data
        
        # Iterate through each answer submitted
        for answer_data in answers_data:
            mcq_question_id = answer_data.get('mcq_question')
            descriptive_question_id = answer_data.get('descriptive_question')

            # Check if an answer already exists for the given questions
            existing_answer = Answer.objects.filter(
                mcq_question__id=mcq_question_id,
                descriptive_question__id=descriptive_question_id
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
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Answers submitted successfully!"}, status=status.HTTP_201_CREATED)