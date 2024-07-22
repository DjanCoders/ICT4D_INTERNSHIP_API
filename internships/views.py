from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import InternshipSerializer, ApplicationSerializer, QuestionSerializer
from .models import Internship, Application, Question
from .permissions import IsAdminOrReadOnly

class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    permission_classes = [IsAdminOrReadOnly]

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(intern=self.request.user)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAdminOrReadOnly]

class ApplyView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer

    def post(self, request, pk):
        internhsip = Internship.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            application = serializer.save(student=request.user, internhsip=internhsip)
            return Response(ApplicationSerializer(application).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)