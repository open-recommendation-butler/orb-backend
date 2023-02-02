from elasticsearch_dsl import Document, InnerDoc, Date, Text, Keyword, Boolean, Integer, DenseVector, analyzer

raw_strip = analyzer('raw_strip',
    tokenizer="whitespace"
)


class Article(Document):
  org_id = Text(
    analyzer=raw_strip,
    fields={'raw': Keyword()}
  )
  title = Text()
  teaser = Text()
  fulltext = Text()
  url = Text(
    analyzer=raw_strip,
    fields={'raw': Keyword()}
  )
  created = Date()
  category = Keyword()
  authors = Text()
  tag_line = Text()
  is_comment = Boolean()
  is_paid = Boolean()
  content_type = Keyword()
  portal = Keyword()
  word_count = Integer()
  is_news_agency = Boolean()
  embedding = DenseVector(
    dims=768
  )

  class Index:
    name = 'article'

class ArticleInner(InnerDoc):
  org_id = Text(
    analyzer=raw_strip,
    fields={'raw': Keyword()}
  )
  title = Text()
  teaser = Text()
  fulltext = Text()
  url = Text(
    analyzer=raw_strip,
    fields={'raw': Keyword()}
  )
  created = Date()
  category = Keyword()
  authors = Text()
  tag_line = Text()
  is_comment = Boolean()
  is_paid = Boolean()
  content_type = Keyword()
  portal = Keyword()
  word_count = Integer()
  is_news_agency = Boolean()
  embedding = DenseVector(
    dims=768
  )