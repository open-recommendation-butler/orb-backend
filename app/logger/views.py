from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .documents import Logger

class LoggerView(APIView):
  def post(self, request, format=None):
    l = Logger(
      name=request.data["name"],
      context=request.data.get("context"),
      log=request.data["log"]
    )
    l.save()
    return Response(status=status.HTTP_201_CREATED)