from elasticsearch_dsl import Document, Date, Text, Keyword, Boolean, Integer, DenseVector, analyzer

raw_strip = analyzer('raw_strip',
    tokenizer="whitespace"
)


class Article(Document):
  title = Text()
  teaser = Text()
  fulltext = Text()
  url = Text(
    analyzer=raw_strip,
    fields={'raw': Keyword()}
  )
  created = Date()
  rubrik_org = Keyword()
  rubrik = Keyword()
  authors = Text()
  tag_line = Text()
  requires_bib = Boolean()
  is_comment = Boolean()
  is_paid = Boolean()
  content_type = Keyword()
  portal = Keyword()
  word_count = Integer()
  is_news_agency = Boolean()
  embedding = DenseVector(
    dims=768,
    #index=True,
    #similarity="dot_product"
  )

  class Index:
    name = 'article'