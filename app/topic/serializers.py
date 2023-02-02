from rest_framework import serializers
from article.serializers import ArticleSerializer

class TopicSerializer(serializers.Serializer):
  title=serializers.CharField()
  article_count=serializers.IntegerField()
  created=serializers.DateTimeField()
  articles=ArticleSerializer(many=True)