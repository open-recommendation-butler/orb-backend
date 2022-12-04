from django.shortcuts import render, redirect
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from article.documents import Article

def search(request):
  print("request.GET.get('q')", request.GET.get('q'))
  queryString = request.GET.get('q')

  # Return to index page if query is empty
  if not queryString:
    return redirect('index')

  query = Article.search().query(
    "multi_match", 
    query=queryString, 
    fields=['title', 'teaser', 'fulltext'],
    fuzziness="AUTO"
  )
  response = query.execute()
  print(response.to_dict())
  context = {
    "articles": query, 
    "queryString": queryString, 
    "took": response.took / 1000, 
    "hitCount": response.hits.total.value
  }
  return render(request, 'search/results.html', context)