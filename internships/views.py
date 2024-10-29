from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import InternshipSerializer, InternshipApplicationSerializer, MCQQuestionSerializer, DescriptiveQuestionSerializer
from .models import MCQQuestion, DescQuestion
from .models import Internship,  MCQQuestion,InternshipApplication
from .permissions import IsAdminOrReadOnly
from django.http import JsonResponse

class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    # permission_classes = [IsAdminOrReadOnly]

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

   def get_queryset(self):
        queryset = InternshipApplication.objects.all()
        status = self.request.query_params.get('status', None)
        
        # Filter by status if the status parameter is provided
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset

def get_applicant_counts(request):
    data={
        'totalApplicants': InternshipApplication.objects.count(),
        'approvedApplicants': InternshipApplication.objects.filter(status='Approved').count(),
        'pendingApplicants': InternshipApplication.objects.filter(status='Pending').count(),
        'rejectedApplicants': InternshipApplication.objects.filter(status='Rejected').count(),
    }
    return JsonResponse(data)