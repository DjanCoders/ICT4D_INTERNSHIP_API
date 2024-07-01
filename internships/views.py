from rest_framework import viewsets

from .serializers import InternshipSerializer, ApplicationSerializer
from .models import Internship, Application
from .permissions import IsAdminOrReadOnly

class InternshipViewSet(viewsets.ModelViewSet):
    queryset = Internship.objects.all()
    serializer_class = InternshipSerializer
    Permission_classes = [IsAdminOrReadOnly]

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminOrReadOnly]