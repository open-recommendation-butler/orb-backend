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
from collections import Counter

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
    topic_day_span = int(request.GET.get('topic_day_span'))

    # Delete all topics from database
    ct = Clear_Topics()
    ct.handle()

    # Generate new topics
    topics = generate_for_all_articles(topic_day_span=topic_day_span)

    # Save topics
    for topic in topics:
      topic_title = None

      categories = [article.category for article in topic.articles]
      keywords = []
      for article in topic.articles:
        try:
          keywords.extend(article.keywords)
        # If article has no keywords
        except TypeError:
          pass

      categories_counted = Counter(categories)
      keywords_counted = Counter(keywords)
      t = Topic(
        title=topic_title,
        created=timezone.now(),
        article_count=len(topic.articles),
        category=categories_counted.most_common(1)[0][0],
        keywords=[x[0] for x in keywords_counted.most_common(3)],
        articles=[
          Article(
            title=a.title,
            teaser=a.teaser,
            url=a.url,
            created=a.created,
            category=a.category,
            content_type=a.content_type,
            portal=a.portal,
            keywords=a.keywords
          ) for a in topic.articles  
        ]
      )
      t.save()

    
    return Response(status=status.HTTP_201_CREATED)