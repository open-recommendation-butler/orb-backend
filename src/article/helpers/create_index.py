from article.documents import Article
from topic.documents import Topic
from suggestion.documents import Suggestion
from logger.documents import Logger
from elasticsearch_dsl import Index

Article.init()
Topic.init()
Suggestion.init()
Logger.init()
print('Index created.')