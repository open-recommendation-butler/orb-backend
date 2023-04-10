from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .documents import Suggestion

class SuggestionView(APIView):
  permission_classes = [permissions.AllowAny]

  def get(self, request, format=None):
    s = Suggestion.search()
    s = s.suggest("auto_complete", request.GET.get('q'), completion={"field": "suggest"})
    response = s.execute()
    res = [x['_source']['name'] for x in response.suggest.auto_complete[0]['options']]
    return Response(res)