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
  highlights = serializers.SerializerMethodField()

  def get_highlights(self, obj):
    highlights = []
    try:
      for highlight in obj.meta.highlight.fulltext:
        timestamp = None
        timestamp_in_seconds = None
        for line in highlight.split('\n')[1:]:
          if '-->' in line:
            timestamp = line.split('.')[0]
            timestamp_in_seconds = int((float(timestamp.split(':')[-1])))
            try:
              timestamp_in_seconds += int(timestamp.split(':')[-2]) * 60
            except ValueError:
              pass
            try:
              timestamp_in_seconds += int(timestamp.split(':')[-3]) * 60 * 60
            except IndexError:
              pass
            break

        highlight = " ".join([x for x in highlight.split('\n') if '-->' not in x])
        highlight = highlight.strip()
        if highlight.endswith('.'):
          highlight += '..'
        else:
          highlight += '...'
        
        highlight = '...' + highlight
        if timestamp:
          highlights.append({
            "timestamp": timestamp,
            "timestamp_in_seconds": timestamp_in_seconds,
            "highlight": highlight
          })
        else:
          highlights.append({"highlight": highlight})
    except AttributeError:
      pass

    if not highlights:
      try:
        highlights.append({"highlight": obj.meta.highlight.teaser[0]})
      except AttributeError:
        try:
          highlights.append({"highlight": obj.teaser})
        except AttributeError:
          highlights.append({"highlight": obj.fulltext[:280]})
    
    return highlights