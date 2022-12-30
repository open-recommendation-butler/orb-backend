from article.documents import Article
import numpy as np
from numpy.linalg import norm

def cosine_sim(a, b):
  return np.dot(a, b)/(norm(a) * norm(b))

def find_topic_recursive(article, articles, already_clustered_articles):
  topic = [article]
  already_clustered_articles.add(article.meta.id)

  for other_article in articles:

    # Ignore already clustered article
    if other_article.meta.id in already_clustered_articles:
      continue

    # Calculate similartiy
    sim = cosine_sim(article.embedding, other_article.embedding)

    # Add the other article to the topic if similarity is over threshold
    if sim > 0.5:

      # Find further similar articles
      t, already_clustered_articles = find_topic_recursive(other_article, articles, already_clustered_articles)
      topic.extend(t)

  return topic, already_clustered_articles

  
def generate(articles):
  topics = []

  # Collect all already clustered articles in a set
  already_clustered_articles = set()

  # Convert embeddings to numpy arrays
  for article in articles:
    article.embedding = np.array(article.embedding)

  # Iterate through articles and create recursive topics
  for article in articles:

    # Ignore already clustered articles
    if article.meta.id in already_clustered_articles:
      continue

    topic, already_clustered_articles = find_topic_recursive(article, articles, already_clustered_articles)
    topics.append(topic)

  return topics

def generate_for_all_articles():
  query = Article.search()
  query = query.query('match_all')
  response = query.execute()

  articles = []

  for i, article in enumerate(query.scan()):
    article.embedding = np.array(article.embedding)
    articles.append(article)
  
  topics = generate(articles)
  return topics