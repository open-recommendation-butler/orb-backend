from article.documents import Article
from elasticsearch_dsl import Q
import dateparser
import numpy as np
from numpy.linalg import norm

def cosine_sim(a, b):
  return np.dot(a, b)/(norm(a) * norm(b))

already_clustered_articles = set()

def find_topic_recursive(article, articles):
  topic = [article]
  already_clustered_articles.add(article.meta.id)
  for other_article in articles:
    if other_article.meta.id in already_clustered_articles:
      continue
    sim = cosine_sim(article.embedding, other_article.embedding)
    if sim > 0.4:
      topic.append(other_article)
      topic.extend(find_topic_recursive(other_article, articles))
  return topic

def generate():
  print('start')
  query = Article.search()
  query = query.query('match_all')

  articles = []
  # Convert article embeddings to numpy arrays
  for article in query.scan():
    print(article.meta.id)
    article.embedding = np.array(article.embedding)
    articles.append(article)
  

  topics = []
  for article in articles:
    if article.meta.id in already_clustered_articles:
      continue
    topics.append(find_topic_recursive(article, articles))
  
  for i, topic in enumerate(topics):
    print()
    print('::::::::::::::::::::::::::::::::::::')
    print(f"TOPIC {i}")
    print('::::::::::::::::::::::::::::::::::::')
    for ii, article in enumerate(topic):
      print(f"ARTICLE {ii}")
      print(article.title)
      print('_')
      print(article.teaser)
      print('_')
      print(article.url)
      print(article.meta.id)

  return