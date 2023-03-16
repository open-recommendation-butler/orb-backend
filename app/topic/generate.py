from article.documents import Article, ArticleInner
import numpy as np
#from .models import Topic
from sklearn.cluster import DBSCAN
from datetime import timedelta
from .documents import Topic
from elasticsearch_dsl import Q
from numpy import dot
from numpy.linalg import norm
import numpy as np
from datetime import timedelta

def sim(a, b):
  return dot(a, b) / (norm(a) * norm(b))

DSBCAN_EPS = 0.35
DBSCAN_MINPTS = 2

def find_topic(article):
  query = Topic.search()
  queryString = "\n".join([x for x in [article.title, article.teaser, article.fulltext] if x])
  query = query.query(
    'bool', 
    must=[
      Q(
        'multi_match', 
        query=queryString[:100], 
        fields=['title^3', 'teaser^2', 'fulltext'], 
        fuzziness="AUTO"
      ),
      Q(
        'range', 
        start_date={'gte': article.created - timedelta(days=3), 'lte': article.created + timedelta(days=3)}
      ),
    ],
  )
  query = query[:40]
  query.execute()
  query = list(query)

  article_embedding = np.array(article.embedding)
  print('query size', len(query))
  for topic in query:
    if topic.article_count == 1:
      continue

    close_pts = 0
    for other_article in topic.articles: 
      if sim(article_embedding, np.array(other_article.embedding)) >= DSBCAN_EPS:
        close_pts += 1
    if close_pts >= DBSCAN_MINPTS:
      topic.add_article(article)
      return
  
  for topic in query:
    if topic.article_count == 1 and sim(article_embedding, topic.articles[0].embedding) >= DSBCAN_EPS:
      topic.add_article(article)
      return
  
  topic = Topic()
  topic.add_article(article)


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