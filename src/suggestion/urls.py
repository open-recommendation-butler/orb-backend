from django.urls import path
from .views import SuggestionView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', SuggestionView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)