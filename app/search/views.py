from elasticsearch_dsl import Q
from article.documents import Article
from topic.documents import Topic
import math
from topic.generate import sort_in_topics
from article.serializers import ArticleSerializer
from topic.serializers import TopicSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from collections import Counter
from django.conf import settings

class SearchView(APIView):
  permission_classes = [permissions.AllowAny]
  
  def get(self, request, format=None):
    ### Get parameters ###

    queryString = request.GET.get('q')

    content_type = request.GET.get('content_type', 'all')

    category = request.GET.get('category')

    publisher = request.GET.get('publisher')

    as_topics = False
    if content_type == 'all' and not publisher and settings.USE_TOPIC_MODELING:
      as_topics = request.GET.get('as_topics', "true").lower() == "true"

    count = int(request.GET.get('count', 20))
    
    page = request.GET.get('page', 1)

    try:
      page = int(page)
    except ValueError:
      # Raise error if page is not an integer
      raise ValidationError("'page' parameter is not an integer.")
    
    # Redirect to first page if page parameter is smaller than 1
    if page < 1:
      raise ValidationError("'page' parameter cannot be negative or 0.")

    if page > 1000:
      raise ValidationError("'page' parameter cannot larger than 1000.")

    # Return to index page if query is empty
    if not queryString:
      raise ValidationError("'q' parameter is missing.")


    ### Execute search in ElasticSearch database ###
    if as_topics:
      query = Topic.search()
      query = query.query(
        'bool', 
        must=[Q('multi_match', query=queryString, fields=['title^3', 'teaser^2', 'fulltext'], fuzziness="AUTO")],
        should=[Q('distance_feature', field="end_date", pivot="100d", origin="now", boost=15)]
      )
    else:
      query = Article.search()
      query = query.query(
        'bool', 
        must=[Q('multi_match', query=queryString, fields=['title^3', 'teaser^2', 'fulltext'])],
        should=[Q('distance_feature', field="created", pivot="100d", origin="now", boost=15)]
      )
      if content_type != 'all':
        query = query.filter('term', content_type=content_type)
      
      if publisher:
        query = query.filter('term', portal=publisher)
      
    if category:
      query = query.filter('term', category=category)

    # Paginate search
    query = query[(page-1)*count:page*count]
    query = query.highlight('teaser', number_of_fragments=1, pre_tags="<em class='font-bold'>", post_tags="</em>", fragment_size=240, boundary_scanner_locale='de-DE')
    query = query.highlight('fulltext', number_of_fragments=5, pre_tags="<em class='font-bold'>", post_tags="</em>", fragment_size=350, boundary_scanner_locale='de-DE')
    
    response = query.execute()
    query = list(query)

    # Raise error if page parameter is bigger than highest possible page
    pageCount = math.ceil(response.hits.total.value / 10)
    if pageCount > 0 and page > pageCount:
      raise ValidationError(f"'page' parameter is bigger than highest possible page. Highest possible page is: {pageCount}")
    
    ### Get similar search requests ###
    similar_search_requests = []
    if as_topics:
      for topic in query:
        for article in topic.articles:
          if article.keywords:
            similar_search_requests.extend(article.keywords)
    else:
      for article in query:
        if article.keywords:
          similar_search_requests.extend(article.keywords)
    similar_search_requests = [x for x in similar_search_requests if x.lower() != queryString.lower()]
    similar_search_requests = [x[0] for x in Counter(similar_search_requests).most_common(6)]

    ### Serialize query ###
    if as_topics:
      content = TopicSerializer(response, many=True).data
    else:
      content = ArticleSerializer(response, many=True).data


    ### Get correction ###
    correct = Article.search().suggest(name="my-suggest", text=queryString, term={'field': 'teaser'})
    correctResponse = correct.execute()

    correction = []
    correction_html = []

    for token in correctResponse.suggest['my-suggest']:
      try:
        correction.append(token['options'][0]['text'])
        correction_html.append(f"<b><i>{token['options'][0]['text']}</i></b>")
      except IndexError:
        correction.append(token['text'])
        correction_html.append(token['text'])

    correction = " ".join(correction)
    correction_html = " ".join(correction_html)
    if correction.lower() == queryString.lower():
      correction = None
      correction_html = None


    ### Create context dictionary ###
    context = {
      "content": content,
      "queryString": queryString, 
      "took": response.took / 1000, 
      "hitCount": response.hits.total.value,
      "as_topics": as_topics,
      "page": page,
      "pageCount": pageCount,
      "similar_search_requests": similar_search_requests,
      "correction": correction,
      "correction_html": correction_html
    }

    return Response(context)