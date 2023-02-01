from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .documents import Topic
from article.documents import Article
from elasticsearch import NotFoundError
from django.http import Http404
from topic.generate import generate_for_all_articles
from django.utils import timezone
from .management.commands.clear_topics import Command as Clear_Topics
from .serializers import TopicSerializer
class TopicView(APIView):
  def get_object(self, pk):
    try:
      a = Topic.get(pk)
      return a
    except NotFoundError:
      raise Http404
  
  def get(self, request, format=None)
    query = Topic.search()
    query = query.query('match_all')
    response = query.execute()
    serializer = TopicSerializer(response, many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    # Delete all topics from database
    ct = Clear_Topics()
    ct.handle()

    # Generate new topics
    topics = generate_for_all_articles()

    # Save topics
    for topic in topics:
      if len(topic.articles) > 1:
        print()
        for article in topic.articles:
          print(article, article.portal, '|', article.title)

      t = Topic(
        title="Topic Title hier",
        created=timezone.now(),
        articles=[
          Article(
            title=a.title,
            teaser=a.teaser,
            url=a.url,
            created=a.created,
            rubrik=a.rubrik,
            content_type=a.content_type,
            portal=a.portal
          ) for a in topic.articles  
        ]
      )
      t.save()

    
    return Response(status=status.HTTP_201_CREATED)