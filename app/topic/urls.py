from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TopicView

urlpatterns = [
    path('', TopicView.as_view()),
    path('<str:pk>/', TopicView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)