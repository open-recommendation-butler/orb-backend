from elasticsearch_dsl import Document, Date, Text, Object
from article.documents import Article

class Topic(Document):
  title = Text()
  teaser = Text()
  created = Date()
  articles = Object(Article, multi=True)

  class Index:
    name = 'topic'