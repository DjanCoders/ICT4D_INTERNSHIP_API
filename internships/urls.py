from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import get_applicant_counts
from .views import (InternshipViewSet #ApplicationViewSet,
                    ,InternshipApplicationView,
                     InternshipApplicationStatusUpdateView,
                     InternshipStatusUpdateView,MCQQuestionViewSet,
                     DescriptiveQuestionViewSet,
                     MonthlyApplicationCountView,
                     UnreadNotificationsView
                     )

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
    path('internships/<int:pk>/status/', InternshipStatusUpdateView.as_view(), name='internship-status-update'),
    path('monthly-application-count/', MonthlyApplicationCountView.as_view(), name='monthly_application_count'),
    path('notifications/',UnreadNotificationsView.as_view(),name="notifications"),
     
]
