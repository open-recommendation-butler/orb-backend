from rest_framework import serializers
from article.serializers import ArticleSerializer

class KeywordsField(serializers.ListField):
    child = serializers.CharField()

class TopicSerializer(serializers.Serializer):
  title=serializers.CharField()
  article_count=serializers.IntegerField()
  category=serializers.CharField(required=False)
  created=serializers.DateTimeField()
  keywords=KeywordsField(required=False)
  articles=ArticleSerializer(many=True)