from elasticsearch_dsl import Document, Date, Text, Object, Integer, Keyword
from article.documents import ArticleInner, Article
import numpy as np
from numpy import dot
from numpy.linalg import norm
from collections import Counter
import json
def sim(a, b):
  return dot(a, b) / (norm(a) * norm(b))

class Topic(Document):
  title = Text()
  teaser = Text()
  fulltext = Text()
  start_date = Date()
  end_date = Date()
  article_count = Integer()
  articles = Object(ArticleInner, multi=True)
  keywords = Keyword(multi=True)
  category = Keyword()

  class Index:
    name = 'topic'
  
  def add_article(self, article):
    if self.article_count:
      self.article_count += 1
    else:
      self.article_count = 1
    
    if self.articles:
      self.articles.append(article)
    else:
      self.articles = [article]

    # Update start and end date
    if not self.start_date or article.created < self.start_date:
      self.start_date = article.created

    if not self.end_date or article.created > self.end_date:
      self.end_date = article.created

    # Find topic mean
    embeddings = [np.array(x.embedding) for x in self.articles]
    mean = np.mean(embeddings, axis=0)

    # Find article closest to topic mean
    similarities = [sim(mean, x) for x in embeddings]
    mean_article = self.articles[np.argmax(similarities)]
    self.title = mean_article.title
    self.teaser = mean_article.teaser
    self.fulltext = mean_article.fulltext

    # Update keywords and category
    all_keywords = []
    all_categories = []
    for article in self.articles:
      if article.keywords:
        all_keywords.extend(article.keywords)
      all_categories.append(article.category)
    counted_keywords = Counter(all_keywords)
    self.keywords = [x[0] for x in counted_keywords.most_common(3)]

    counted_categories = Counter(all_categories)
    self.category = counted_categories.most_common(1)[0][0]
    
    self.save()