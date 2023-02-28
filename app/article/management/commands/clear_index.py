from django.core.management.base import BaseCommand
from article.documents import Article
from elasticsearch_dsl import Index

class Command(BaseCommand):
  help = 'Wipes out your entire search index. Use with caution.'

  def add_arguments(self, parser):
    pass

  def handle(self, *args, **options):
    self.stdout.write(
      "Removing all documents from your index because you said so."
    )
    indx = Index('article')
    indx.delete()

    Article.init()
    self.stdout.write(
      "Done."
    )