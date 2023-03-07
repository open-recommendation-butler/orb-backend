from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

class PortalView(APIView):
  def get(self, request, format=None):
    s = Search()
    s = Search.from_dict({
        "aggs": {
            "portals": {
                "terms": {
                  "field": "portal",
                  "size": 50
                }
            }
        }
    })
    s = s[:0]

    response = s.execute()
    portals = [x.key for x in response.aggregations.portals.buckets]
    return Response(portals)