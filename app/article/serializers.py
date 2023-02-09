from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
  org_id = serializers.CharField(required=False)
  title = serializers.CharField(required=False)
  teaser = serializers.CharField(required=False)
  portal = serializers.CharField(required=False)
  category = serializers.CharField(required=False)
  content_type = serializers.CharField(required=False)
  keywords = serializers.CharField(required=False)
  url = serializers.URLField(required=False)
  created = serializers.DateTimeField(required=False)