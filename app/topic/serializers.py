from rest_framework import serializers

class TopicSerializer(serializers.Serializer):
  title=serializers.CharField()