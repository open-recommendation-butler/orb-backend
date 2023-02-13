from django.db import models
from collections import Counter
class Topic:
  def __init__(self):
    self.articles = []
    self.article_count = None
    self.keywords = []
  
  def get_keywords(self):
    all_occurences = []
    for article in self.articles:
      all_occurences.extend(article.keywords)
    counted = Counter(all_occurences)
    self.keywords = [x[0] for x in counted.most_common()]
  
  def get_article_count(self):
    self.article_count = len(self.articles)