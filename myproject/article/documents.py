from elasticsearch_dsl import Document, Date, Text


class Article(Document):
  title = Text()
  teaser = Text()
  fulltext = Text()
  url = Text()
  created = Date()

  class Index:
    name = 'article'