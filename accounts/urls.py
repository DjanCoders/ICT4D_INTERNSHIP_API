from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CustomUserViewSet, ProfileViewSet, RegisterView

router = DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('profiles', ProfileViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]