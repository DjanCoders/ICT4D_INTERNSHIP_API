from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InternshipViewSet, ApplicationViewSet, QuestionViewSet, ApplyView

router = DefaultRouter()
router.register('internships', InternshipViewSet)
router.register('applications', ApplicationViewSet)
router.register('questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('internships/<int:pk>/apply/', ApplyView.as_view(), name='apply'),
]