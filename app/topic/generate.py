from article.documents import Article
import numpy as np
from .models import Topic
from sklearn.cluster import DBSCAN
from datetime import timedelta

def sort_in_topics(articles, topic_day_span=7):
  if len(articles) == 0:
    return []
  
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
    if key == -1:
      for article in value:
        t = Topic()
        t.add_article(article)
        topic_list.append(t)
    else:
      time_spans = []
      for article in value:
        found = False
        for t in time_spans:
          if article.created \
          and article.created < (t.end_date + timedelta(days=topic_day_span)) \
          and article.created > (t.start_date - timedelta(days=topic_day_span)):
            t.add_article(article)
            found = True
            break
        if not found:
          t = Topic()
          t.add_article(article)
          time_spans.append(t)

      topic_list.extend(time_spans)

  return topic_list


def generate_for_all_articles(topic_day_span=None):
  query = Article.search()
  if topic_day_span:
    query = query.query('range', created={'gte': f'now-{topic_day_span}d/d'})
  else:
    query = query.query('match_all')
  response = query.execute()
  
  articles = [a for a in query.scan()]

  return sort_in_topics(articles)