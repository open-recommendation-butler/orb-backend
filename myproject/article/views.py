from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .documents import Article
from .serializers import ArticleSerializer
from elasticsearch import NotFoundError
from django.http import Http404
from django.conf import settings
class ArticleView(APIView):
  """
  Retrieve, update or delete an article instance.
  """
  def get_object(self, pk):
    try:
      a = Article.get(pk)
      return a
    except NotFoundError:
      raise Http404

  def get(self, request, pk, format=None):
    a = self.get_object(pk)
    serializer = ArticleSerializer(a)
    return Response(serializer.data)

  def post(self, request, format=None):

    # Create a new article document and save it to the ElasticSearch database
    a = Article(
      title=request.data.get("title"),
      teaser=request.data.get("teaser"),
      fulltext=request.data.get("fulltext"),
      url=request.data.get("url"),
      created=request.data.get("created")
    )

    # Add the embedding
    a.embedding = list(
      settings.MODEL.encode(
        "\n\n".join(
            [x for x in (a.title, a.teaser, a.fulltext) if x]
          )
      )
    )

    # Save the article
    a.save()

    return Response(status=status.HTTP_201_CREATED)


  def delete(self, request, pk, format=None):
      a = self.get_object(pk)
      a.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)