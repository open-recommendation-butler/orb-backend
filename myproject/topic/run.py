from topic.generate import generate_for_all_articles
import time

start = time.time()
topics = generate_for_all_articles()
print(topics)
end = time.time()

for topic in topics:
  if len(topic.articles) > 1:
    print()
    for article in topic.articles:
      print(article.portal, '|', article.title)

print(f'Time:', end - start)