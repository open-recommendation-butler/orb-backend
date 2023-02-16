from django.shortcuts import render, redirect
from elasticsearch_dsl import Q
from article.documents import Article
import math
from topic.generate import sort_in_topics
from article.serializers import ArticleSerializer
from topic.serializers import TopicSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import time

class SearchView(APIView):
  permission_classes = [permissions.AllowAny]
  
  def get(self, request, format=None):
    ### Get parameters ###

    queryString = request.GET.get('q')

    as_topics = request.GET.get('as_topics', True)

    topic_day_span = int(request.GET.get('topic_day_span', 7))

    content_type = request.GET.get('content_type', 'article')

    count = int(request.GET.get('count', 20))

    # Default to "article" as content type if no valid content type is provided
    if content_type not in ['podcast', 'gallery', 'multimedia']:
      content_type = 'article'
    
    page = request.GET.get('page', 1)

    try:
      page = int(page)
    except ValueError:
      # Redirect to first page if page parameter is not a number
      return redirect(f'/search/?q={queryString}&content_type={content_type}')
    
    # Redirect to first page if page parameter is smaller than 1
    if page < 1:
      redirect(f'/search/?q={queryString}&content_type={content_type}')

    if page > 1000:
      page = 1000

    # Return to index page if query is empty
    if not queryString:
      return redirect('index')


    ### Execute search in ElasticSearch database ###

    query = Article.search()
    query = query.query(
      'bool', 
      must=[
        Q('multi_match', query=queryString, fields=['title^3', 'teaser^2', 'fulltext'], fuzziness="AUTO"),
        #Q('term', content_type=content_type)
      ],
      should=[
        # Q('match', is_paid=True), 
        # Q('match', is_news_agency=False),
        Q('distance_feature', field="created", pivot="600d", origin="now", boost=15)
      ]
    )

    # Query a lot of articles if they are supposed to be sorted in topics
    if as_topics:
      query = query[:100]

    # Else paginate search
    else:
      query = query[(page-1)*count:page*count]
    
    start = time.time()
    response = query.execute()
    query = list(query)
    print('Transfer Time:', time.time() - start)
    ### Check for suggestions to fix typos made by users ###

    suggest = Article.search().suggest(name="my-suggest", text=queryString, term={'field': 'teaser'})
    suggestResponse = suggest.execute()

    suggestion = []
    suggestion_html = []

    for token in suggestResponse.suggest['my-suggest']:
      try:
        suggestion.append(token['options'][0]['text'])
        suggestion_html.append(f"<b><i>{token['options'][0]['text']}</i></b>")
      except IndexError:
        suggestion.append(token['text'])
        suggestion_html.append(token['text'])

    suggestion = " ".join(suggestion)
    suggestion_html = " ".join(suggestion_html)
    if suggestion.lower() == queryString.lower():
      suggestion = None
      suggestion_html = None

    ### Execute checks ###

    # Redirect to highest possible page if page parameter is bigger than highest possible page
    pageCount = None
    if not as_topics:
      pageCount = math.ceil(response.hits.total.value / 10)
      if pageCount > 0 and page > pageCount:
        return redirect(f'/search/?q={queryString}&content_type={content_type}&page={pageCount}')
    
    ### Sort in topics ###
    if as_topics:
      start = time.time()
      query = sort_in_topics(query, topic_day_span=topic_day_span)
      print('Zeit:', time.time() - start)
      # Sort topics by sum of their scores
      query.sort(key=lambda topic: sum([article.meta.score for article in topic.articles]) / len(topic.articles), reverse=True)

      hitCount = len(query)
      query = query[(page - 1) * count:page * count]
      content = TopicSerializer(query, many=True).data
    else:
      content = ArticleSerializer(query, many=True).data
      hitCount = response.hits.total.value

    ### Create context dictionary ###
    context = {
      "content": content,
      "queryString": queryString, 
      "took": (response.took + suggestResponse.took) / 1000, 
      "hitCount": hitCount,
      "suggestion": suggestion,
      "suggestion_html": suggestion_html,
      "content_type": content_type,
      "page": page,
      "pageCount": pageCount
    }

    return Response(context)