from django.core.management.base import BaseCommand
from article.documents import Article

class Command(BaseCommand):
  help = 'Deletes all new articles from database. Use with caution.'

  def add_arguments(self, parser):
    pass

  def handle(self, *args, **options):
    query = Article.search()
    query = query.query('range', created={'gte': f'now-3d/d'})
    response = query.execute()
    
    res = list(query.scan())
    for i, article in enumerate(res):
      article.delete()
      print(f'Deleted: {i}/{len(res)}')