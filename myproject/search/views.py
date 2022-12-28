from django.shortcuts import render, redirect
from elasticsearch_dsl import Q
from article.documents import Article
import math

def search(request):
  print("request.GET.get('q')", request.GET.get('q'))
  queryString = request.GET.get('q')
  content_type = request.GET.get('content_type', 'article')
  if content_type not in ['podcast', 'gallery', 'multimedia']:
    content_type = 'article'
  page = request.GET.get('page', 1)
  try:
    page = int(page)
  except ValueError:
    return redirect(f'/search/?q={queryString}&content_type={content_type}')
  if page < 1:
    redirect(f'/search/?q={queryString}&content_type={content_type}')
  if page > 1000:
    page = 1000

  # Return to index page if query is empty
  if not queryString:
    return redirect('index')

  query = Article.search()
  # .query(
  #   "multi_match", 
  #   query=queryString, 
  #   fields=['title', 'teaser', 'fulltext'],
  #   fuzziness="AUTO"
  # ).filter('term', content_type=content_type)
  query = query.query(
    'bool', 
    must=[
      Q('multi_match', query=queryString, fields=['title', 'teaser', 'fulltext'], fuzziness="AUTO"),
      #Q('term', content_type=content_type)
    ],
    should=[Q('match', is_paid=True), Q('match', is_news_agency=False)]
  )
  query = query[(page-1)*10:page*10]
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
  if suggestion.lower() == queryString.lower():
    suggestion = None
    suggestion_html = None

  pageCount = math.ceil(response.hits.total.value / 10)
  if pageCount > 0 and page > pageCount:
    print(f'/search/?q={queryString}&content_type={content_type}&page={pageCount}')
    return redirect(f'/search/?q={queryString}&content_type={content_type}&page={pageCount}')
  context = {
    "articles": query, 
    "queryString": queryString, 
    "took": (response.took + suggestResponse.took) / 1000, 
    "hitCount": response.hits.total.value,
    "suggestion": suggestion,
    "suggestion_html": suggestion_html,
    "content_type": content_type,
    "page": page,
    "pageCount": pageCount
  }
  return render(request, 'search/results.html', context)