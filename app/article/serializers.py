from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  title = serializers.CharField(required=False, allow_blank=True)
  teaser = serializers.CharField(required=False, allow_blank=True)
  portal = serializers.CharField(required=False, allow_blank=True)
  category = serializers.CharField(required=False, allow_blank=True)
  content_type = serializers.CharField(required=False, allow_blank=True)
  url = serializers.URLField()
  created = serializers.DateTimeField()