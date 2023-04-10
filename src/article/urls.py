from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ArticleView

urlpatterns = [
    path('', ArticleView.as_view()),
    path('<str:org_id>/', ArticleView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)