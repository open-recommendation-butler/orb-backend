from django.core.management.base import BaseCommand
from article.documents import Article
from topic.documents import Topic
from suggestion.documents import Suggestion
from elasticsearch_dsl import Index
from elasticsearch.exceptions import NotFoundError

class Command(BaseCommand):
  help = 'Wipes out your entire search index. Use with caution.'

  def add_arguments(self, parser):
    pass

  def handle(self, *args, **options):
    self.stdout.write(
      "Removing all documents from your index because you said so."
    )
    for index_name in ('article', 'topic', 'suggestion'):
      try:
        index = Index(index_name)
        index.delete()
        self.stdout.write(f'Deleted "{index_name}" index.')
      except NotFoundError:
        self.stdout.write(f'Index "{index_name}" does not exist.')

    Article.init()
    Topic.init()
    Suggestion.init()
    self.stdout.write(
      'Done: Successfully recreated "article", "topic", and "suggestion" index.'
    )