from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import get_applicant_counts
from .views import (InternshipViewSet #ApplicationViewSet,
                     ,MCQQuestionViewSet, DescriptiveQuestionViewSet,InternshipApplicationView, InternshipApplicationStatusUpdateView)

router = DefaultRouter()
router.register('internships', InternshipViewSet)
#router.register('applications', ApplicationViewSet)
router.register('mcqquestions', MCQQuestionViewSet)
router.register('shortanswerquestions', DescriptiveQuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('internships/<int:pk>/apply/', ApplyView.as_view(), name='apply'),
    path('internship-application/',InternshipApplicationView.as_view(),name='internship-application'),
    path('applicant_counts/',get_applicant_counts,name="applicant-counts"),
    path('internship-applications/<int:pk>/status/', InternshipApplicationStatusUpdateView.as_view(), name='internship-status-update'),

]
