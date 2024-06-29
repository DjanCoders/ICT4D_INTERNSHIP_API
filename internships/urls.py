from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_internship/', views.create_internship, name='create_internship'),
]
