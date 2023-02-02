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
from django.conf import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

class TopicView(APIView):
  def get_object(self, pk):
    try:
      a = Topic.get(pk)
      return a
    except NotFoundError:
      raise Http404
  
  def get(self, request, format=None):
    query = Topic.search()
    query = query.query('match_all')
    response = query.execute()
    print(query)
    serializer = TopicSerializer(query.scan(), many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    # Delete all topics from database
    ct = Clear_Topics()
    ct.handle()

    # Generate new topics
    topics = generate_for_all_articles()

    # Save topics
    for topic in topics:
      topic_title = None

      if len(topic.articles) > 1:
        print()
        for article in topic.articles:
          print(article, article.portal, '|', article.title)

        if settings.OPENAI_API_KEY:
          topic_title = openai.Completion.create(
            model="text-davinci-003", 
            prompt=f'Paraphrasiere in wenigen Wörtern: "{topic.articles[0].title}"', 
            temperature=0.7, 
            max_tokens=30
          )
          topic_title = topic_title.choices[0].text
          topic_title = topic_title.strip()
          if topic_title.endswith('.'):
            topic_title = topic_title[:-1]
          print('TITLE:', topic_title)

      t = Topic(
        title=topic_title,
        created=timezone.now(),
        article_count=len(topic.articles),
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