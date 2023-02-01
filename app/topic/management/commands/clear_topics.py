from django.core.management.base import BaseCommand, CommandError
from topic.documents import Topic
from elasticsearch_dsl import Index

class Command(BaseCommand):
  help = 'Wipes out your entire topic index. Use with caution.'

  def add_arguments(self, parser):
    pass

  def handle(self, *args, **options):
    self.stdout.write(
      "Removing all topics from your index because you said so."
    )
    indx = Index('topic')
    indx.delete()

    Topic.init()
    self.stdout.write(
      "Done."
    )