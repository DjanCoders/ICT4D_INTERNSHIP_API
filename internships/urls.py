from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import get_applicant_counts
from .views import (InternshipViewSet #ApplicationViewSet,
                    ,InternshipApplicationView,
                     InternshipApplicationStatusUpdateView,
                     InternshipStatusUpdateView,MCQQuestionViewSet,
                     DescriptiveQuestionViewSet,
                     MonthlyApplicationCountView,
                     UnreadNotificationsView,
                     GetQuestionsAPIView,
                     SubmitAnswersAPIView,
                     AnswerListView,
                     TopScorersAPIView,
                     ExamSettingsViewSet,
                     end_exam_duration
                     )

router = DefaultRouter()
router.register('internships', InternshipViewSet)
router.register('internship-application', InternshipApplicationView)
router.register('mcqquestions', MCQQuestionViewSet)
router.register('shortanswerquestions', DescriptiveQuestionViewSet)
router.register('exam-settings', ExamSettingsViewSet),


urlpatterns = [
    path('', include(router.urls)),
    # path('internships/<int:pk>/apply/', ApplyView.as_view(), name='apply'),
    # path('internship-application/',InternshipApplicationView.as_view(),name='internship-application'),
    path('applicant_counts/',get_applicant_counts,name="applicant-counts"),
    path('internship-applications/<int:pk>/status/', InternshipApplicationStatusUpdateView.as_view(), name='internship-status-update'),
    path('internships/<int:pk>/status/', InternshipStatusUpdateView.as_view(), name='internship-status-update'),
    path('monthly-application-count/', MonthlyApplicationCountView.as_view(), name='monthly_application_count'),
    path('notifications/',UnreadNotificationsView.as_view(),name="notifications"),
    path('get-questions/',GetQuestionsAPIView.as_view(), name="get-questions"),
    path('submit-answers/',SubmitAnswersAPIView.as_view(), name="submit-answers"),
    path('review-answers/', AnswerListView.as_view(), name='review-answers'),
    path('review-answers/<int:pk>/', AnswerListView.as_view(), name='answer-detail'),
    path('top-scorers/', TopScorersAPIView.as_view(), name='top-scorers'),
   
   path('end_exam_duration/<int:category_id>/', end_exam_duration, name='end_exam_duration'),






     
]
