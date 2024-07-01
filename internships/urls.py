from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InternshipViewSet, ApplicationViewSet

router = DefaultRouter()
router.register('internships', InternshipViewSet)
router.register('applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]