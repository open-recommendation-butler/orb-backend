from elasticsearch_dsl import Document, Integer, analyzer, Completion, token_filter, Keyword
from itertools import permutations

# custom analyzer for names
ascii_fold = analyzer(
    "ascii_fold",
    # we don't want to split O'Brian or Toulouse-Lautrec
    tokenizer="whitespace",
    filter=["lowercase", token_filter("ascii_fold", "asciifolding")],
)

class Suggestion(Document):
  name = Keyword()
  suggest = Completion(analyzer=ascii_fold)
  occurences = Integer()

  def clean(self):
    """
    Automatically construct the suggestion input and weight by taking all
    possible permutation of Person's name as ``input`` and taking their
    occurences as ``weight``.
    """
    self.suggest = {
      "input": [" ".join(p) for p in permutations(self.name.split())],
      "weight": self.occurences
    }

  class Index:
    name = 'suggestion'