from rest_framework import serializers
from article.serializers import ArticleSerializer

class KeywordsField(serializers.ListField):
    child = serializers.CharField()

class TopicSerializer(serializers.Serializer):
  type=serializers.CharField(default="topic")
  title=serializers.CharField(required=False)
  article_count=serializers.IntegerField()
  category=serializers.CharField(required=False)
  created=serializers.DateTimeField(required=False)
  keywords=KeywordsField(required=False)
  articles=ArticleSerializer(many=True)