from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .documents import Article
from .serializers import ArticleSerializer
from django.http import Http404
from django.conf import settings
from topic.generate import find_topic
import dateparser
from article.helpers.get_keywords import get_keywords

class ArticleView(APIView):
  """
  Retrieve, update or delete an article instance.
  """
  def get_object(self, org_id):
    query = Article.search()
    query = query.filter('term', org_id=org_id)
    query.execute()
    query = list(query)
    if query:
      return query[0]

    return None

  def get(self, request, org_id, format=None):
    a = self.get_object(org_id)
    if not a:
      raise Http404
    serializer = ArticleSerializer(a)
    return Response(serializer.data)

  def save(self, entry):
    # Create a new article document and save it to the ElasticSearch database
    fulltext = entry.get("fulltext")
    if fulltext:
      fulltext = fulltext[:8000]
    a = Article(
      org_id=entry.get("org_id"),
      title=entry.get("title"),
      teaser=entry.get("teaser"),
      fulltext=fulltext,
      url=entry.get("url"),
      created=dateparser.parse(entry.get("created")),
      content_type=entry.get("content_type"),
      portal=entry.get("portal"),
      category=entry.get("category"),
      is_paid=entry.get("is_paid")
    )

    # Add the embedding
    a.embedding = list(
      settings.MODEL.encode(
        "\n\n".join(
            [x for x in (a.title, a.teaser, a.fulltext) if x]
          )
      )
    )

    a.keywords = get_keywords(
      "\n\n".join(
        [x for x in (a.title, a.teaser, a.fulltext) if x]
      )
    )

    # Save the article
    a.save()

    find_topic(a)

  def post(self, request, format=None):

    # Ignore articles whose url is already in the database
    if request.data.get("url") and request.data.get('content_type') == 'article':
      query = Article.search().filter("term", url=request.data.get("url"))
      response = query.execute()
      if response.hits.total.value != 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Ignore articles whose id is already in the database
    if request.data.get("org_id") and self.get_object(request.data.get("org_id")):
      return Response(status=status.HTTP_400_BAD_REQUEST)

    if isinstance(request.data, list):
      for i, entry in enumerate(request.data):
        self.save(entry)
    else:
      self.save(request.data)

    return Response(status=status.HTTP_201_CREATED)


  def delete(self, request, pk, format=None):
      a = self.get_object(pk)
      a.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)