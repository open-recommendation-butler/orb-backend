from elasticsearch_dsl import Document, InnerDoc, Date, Text, Keyword, Boolean, Integer, DenseVector, analyzer, Completion, token_filter
from article.helpers.get_keywords import get_keywords
from suggestion.documents import Suggestion
from django.utils import timezone

class Logger(Document):
  name = Keyword()
  log = Text()
  context = Text()
  created = Date()

  def save(self):
    self.created = timezone.now()
    super().save()

  class Index:
    name = 'logger'