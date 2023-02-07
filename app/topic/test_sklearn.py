import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.metrics.pairwise import cosine_similarity
from article.documents import Article

query = Article.search()
query = query.query('match_all')
response = query.execute()

articles = [a for a in query.scan()]
# X = [a.embedding for a in articles]
# X = np.array(X)

# EPS = 6
# MIN_SAMPLES = 2

# db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(X)
# labels = db.labels_

# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# n_noise_ = list(labels).count(-1)

# print()
# print("Estimated number of clusters: %d" % n_clusters_)
# print("Estimated number of noise points: %d" % n_noise_)

# topics = {}
# for i, label in enumerate(labels):
#   try:
#     topics[label].append(articles[i])
#   except KeyError:
#     topics[label] = [articles[i]]

# for key, value in topics.items():
#   if key != -1:

#     print()
#     for article in value:
#       print(article.title)

for article in articles:
  if 'rbb|24 ist das multimediale Nachrichtenportal' in article.teaser:
    for other_article in articles:
      if article.title != other_article.title and 'rbb|24 ist das multimediale Nachrichtenportal' in other_article.teaser:
        print()
        print(article.title)
        print()
        print(article.teaser)
        print()
        print(other_article.title)
        print()
        print(other_article.teaser)
        print()
        print('SIM', cosine_similarity([article.embedding, other_article.embedding]))