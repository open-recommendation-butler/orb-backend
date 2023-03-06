from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
  type=serializers.CharField(default="article")
  org_id = serializers.CharField(required=False)
  title = serializers.CharField(required=False)
  teaser = serializers.CharField(required=False)
  portal = serializers.CharField(required=False)
  category = serializers.CharField(required=False)
  content_type = serializers.CharField(required=False)
  keywords = serializers.ListField(required=False)
  url = serializers.URLField(required=False)
  created = serializers.DateTimeField(required=False)