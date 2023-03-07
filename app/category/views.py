from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

class CategoryView(APIView):
  def get(self, request, format=None):
    s = Search()
    s = Search.from_dict({
        "aggs": {
            "categories": {
                "terms": {
                  "field": "category",
                  "size": 50
                }
            }
        }
    })
    s = s[:0]

    response = s.execute()
    categories = [x.key for x in response.aggregations.categories.buckets]
    return Response(categories)