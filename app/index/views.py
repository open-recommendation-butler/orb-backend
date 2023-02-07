from django.shortcuts import render
from article.documents import Article
from elasticsearch_dsl import Search, A

def index(request):
  s = Search()
  a = A('terms', field='category')
  s.aggs.bucket('terms', a)
  print(s.to_dict())
  response = s.execute()
  for hit in response:
    print(hit)

  # print(response)
  # portals = [a.portal for a in response]
  # print(response['hits'])
  context= {}
  return render(request, 'index/index.html', context)

def imprint(request):
  return render(request, 'index/imprint.html')