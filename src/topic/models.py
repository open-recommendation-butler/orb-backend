from django.db import models
from collections import Counter
class Topic:
  def __init__(self):
    self.articles = []
    self.article_count = 0
    self.keywords = []
    self.start_date = None
    self.end_date = None
  
  def add_article(self, article):
    self.articles.append(article)
    self.article_count += 1
    if article.created:
      if self.start_date:
        self.start_date = min(self.start_date, article.created)
      else:
        self.start_date = article.created
      
      if self.end_date:
        self.end_date = max(self.end_date, article.created)
      else:
        self.end_date = article.created
    self.get_keywords()
  
  def get_keywords(self):
    all_occurences = []
    for article in self.articles:
      if article.keywords:
        all_occurences.extend(article.keywords)
    counted = Counter(all_occurences)
    self.keywords = [x[0] for x in counted.most_common()]