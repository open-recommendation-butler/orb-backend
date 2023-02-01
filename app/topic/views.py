from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .documents import Topic
from elasticsearch import NotFoundError
from django.http import Http404
from topic.generate import generate_for_all_articles
class TopicView(APIView):
  def get_object(self, pk):
    try:
      a = Topic.get(pk)
      return a
    except NotFoundError:
      raise Http404

  def post(self, request, format=None):
    topics = generate_for_all_articles()

    for topic in topics:
      if len(topic.articles) > 1:
        print()
        for article in topic.articles:
          print(article.portal, '|', article.title)
    
    return Response(status=status.HTTP_201_CREATED)