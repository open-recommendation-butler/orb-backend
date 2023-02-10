import pickle

with open('article/helpers/keywords.pickle', 'rb') as file:
  keywords_dict = pickle.load(file)

with open('article/helpers/keyword_redirects.pickle', 'rb') as file:
  keyword_redirects_dict = pickle.load(file)

with open('article/helpers/vornamen.pickle', 'rb') as file:
  vornamen_set = pickle.load(file)

forbidden_entities = vornamen_set
forbidden_entities.update(['Die', 'Auch', 'Es', 'Traum', 'Problem', 'Heute', 'Woche', 'Tag', 'Jahr',
  'Wochenende', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag',
  'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober',
  'November', 'Dezember',
  'Zahlen', 'Sind', 'Nachrichten', 'Politik', 'Wirtschaft', 'Sonstiges', 'Umwelt', 'Kunst', 'Kultur',
  'Sport'
])

def get_keywords(text):
  for sign in ['.', '?', '!', ':']:
    text = text.replace(sign, '')
  
  words = text.split()
  keywords = set()
  for i in range(0, len(words)):
    if any(char.isupper() for char in words[i]):
      entity = " ".join(words[i:i+4]) + " "
      while " " in entity:
        entity = " ".join(entity.split(' ')[:-1])
        try:
          keywords_dict[entity]
          keywords.add(entity)
          break
        except KeyError:
          try:
            keyword_redirects_dict[entity]
            keywords.add(entity)
            break
          except KeyError:
            pass
    
    # Clean keywords
    cleaned = []
    for kw in keywords:
      if len(kw) < 3:
        continue

      if kw in forbidden_entities:
        continue
      
      if kw in " ".join([x for x in keywords if x != kw]):
        continue

      cleaned.append(kw)
      
  return cleaned