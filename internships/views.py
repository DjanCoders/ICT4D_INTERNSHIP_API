from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import InternshipSerializer, InternshipApplicationSerializer, MCQQuestionSerializer, DescriptiveQuestionSerializer
from .models import( Internship, MCQQuestion, 
                    MCQQuestion,InternshipApplication,
                    Notification,DescQuestion)
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


# class ApplicationViewSet(viewsets.ModelViewSet):
#     queryset = Application.objects.all()
#     serializer_class = ApplicationSerializer
#     # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(intern=self.request.user)
class MCQQuestionViewSet(viewsets.ModelViewSet):
    queryset = MCQQuestion.objects.all()
    serializer_class = MCQQuestionSerializer
    permission_classes = [IsAdminOrReadOnly]

class DescriptiveQuestionViewSet(viewsets.ModelViewSet):
    queryset = DescQuestion.objects.all()
    serializer_class = DescriptiveQuestionSerializer
    permission_classes = [IsAdminOrReadOnly]


# class ApplyView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ApplicationSerializer

#     def post(self, request, pk):
#         internhsip = Internship.objects.get(pk=pk)
#         serializer = self.get_serializer(data=request.data)
        
#         if serializer.is_valid():
#             application = serializer.save(student=request.user, internhsip=internhsip)
#             return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class InternshipApplicationView(generics.ListCreateAPIView):
   serializer_class = InternshipApplicationSerializer
   queryset = InternshipApplication.objects.all()


   def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get('status', None)
        
        # Filter by status if the status parameter is provided
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
   def create(self, request, *args, **kwargs):
        email = request.data.get('email')  # Extract the email from the request data
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if an application with this email already exists
        try:
            existing_application = InternshipApplication.objects.get(email=email)
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
    
