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

  suggest = Article.search().suggest(name="my-suggest", text=queryString, term={'field': 'teaser'})
  suggestResponse = suggest.execute()
  print('suggestResponse', suggestResponse.to_dict())
  suggestion = []
  suggestion_html = []
  print('___')
  for token in suggestResponse.suggest['my-suggest']:
    try:
      suggestion.append(token['options'][0]['text'])
      suggestion_html.append(f"<b><i>{token['options'][0]['text']}</i></b>")
    except IndexError:
      suggestion.append(token['text'])
      suggestion_html.append(token['text'])

  suggestion = " ".join(suggestion)
  suggestion_html = " ".join(suggestion_html)
  if suggestion == queryString:
    suggestion = None
    suggestion_html = None


  context = {
    "articles": query, 
    "queryString": queryString, 
    "took": (response.took + suggestResponse.took) / 1000, 
    "hitCount": response.hits.total.value,
    "suggestion": suggestion,
    "suggestion_html": suggestion_html
  }
  return render(request, 'search/results.html', context)