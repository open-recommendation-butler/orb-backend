from article.documents import Article
import numpy as np
from .models import Topic
from sklearn.cluster import DBSCAN


def sort_in_topics(articles):
  X = [a.embedding for a in articles]
  X = np.array(X)

  EPS = 6
  MIN_SAMPLES = 2

  db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
  labels = db.labels_

  topics = {}
  for i, label in enumerate(labels):
    try:
      topics[label].append(articles[i])
    except KeyError:
      topics[label] = [articles[i]]

  topic_list = []
  for key, value in topics.items():
    if key != -1:
      print()
      t = Topic()
      for article in value:
        print(article.title)
        t.articles.append(article)
        t.get_keywords()
        t.get_article_count()
      topic_list.append(t)

  return topic_list


def generate_for_all_articles():
  query = Article.search()
  query = query.query('match_all')
  response = query.execute()
  
  articles = [a for a in query.scan()]

  return sort_in_topics(articles)