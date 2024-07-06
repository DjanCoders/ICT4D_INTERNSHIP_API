from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InternshipViewSet, ApplicationViewSet, QuestionViewSet

router = DefaultRouter()
router.register('internships', InternshipViewSet)
router.register('applications', ApplicationViewSet)
router.register('questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]