from elasticsearch_dsl import Document, Date, Text, Object, Integer
from article.documents import ArticleInner

class Topic(Document):
  title = Text()
  teaser = Text()
  created = Date()
  article_count = Integer()
  articles = Object(ArticleInner, multi=True)

  class Index:
    name = 'topic'