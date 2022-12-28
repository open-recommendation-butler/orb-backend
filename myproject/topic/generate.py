from article.documents import Article
from elasticsearch_dsl import Q
import dateparser
import numpy as np
from numpy.linalg import norm

def cosine_sim(a, b):
  return np.dot(a, b)/(norm(a) * norm(b))

def generate():
  print('start')
  query = Article.search()
  query = query.query(
    'bool', 
    must=[
      Q('term', created=dateparser.parse("28.12.2022", settings={'DATE_ORDER': 'DMY'})),
      #Q('term', content_type=content_type)
    ]
  )
  # response = query.scan()

  articles = []
  # Convert article embeddings to numpy arrays
  for article in query.scan():
    #print(article.meta.id)
    article.embedding = np.array(article.embedding)
    articles.append(article)
  
  
  checked_articles = set()
  for article in articles:
    if article.meta.id in checked_articles:
      continue
    checked_articles.add(article.meta.id)
    other_articles = []
    for other_article in articles:
      if other_article.meta.id in checked_articles:
        continue
      sim = cosine_sim(article.embedding, other_article.embedding)
      if sim > 0.4:
        other_articles.append(other_article)
        checked_articles.add(other_article.meta.id)
        print()
        print()
        print(article.title)
        print(article.teaser)
        print('####')
        print('____________________')
        print(other_article.title)
        print(other_article.teaser)
        print('Sim', sim)

  return