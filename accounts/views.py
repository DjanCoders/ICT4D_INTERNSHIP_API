from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Profile
from .serializers import CustomUserSerializer, ProfileSerializer, RegisterationSerializer
from .permissions import IsOwner

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': CustomUserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

