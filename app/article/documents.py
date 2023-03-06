from elasticsearch_dsl import Document, InnerDoc, Date, Text, Keyword, Boolean, Integer, DenseVector, analyzer, Completion, token_filter, Float
from article.helpers.get_keywords import get_keywords
from suggestion.documents import Suggestion
from django.conf import settings

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
  keywords = Keyword()
  embedding = DenseVector(
    dims=768,
    multi=True
  )

  def save(self):
    super().save()

    # Iterate through all keywords
    for keyword in self.keywords:

      # Check if keyword is already in the suggestion index
      query = Suggestion.search()
      query = query.filter('term', name=keyword)
      query.execute()
      query = list(query)

      # If its in the index increment the occurences count
      # Else: Create new enty
      if query:
        query[0].occurences += 1
        query[0].save()
      else:
        s = Suggestion(name=keyword, occurences=1, embedding=list(settings.MODEL.encode(keyword)))
        s.save()

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
  keywords = Keyword()
  embedding = Float()