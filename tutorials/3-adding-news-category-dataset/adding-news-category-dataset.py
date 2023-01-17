import opendatasets
import json
import requests

# Download dataset from kaggle and save it to the folger news-category-dataset
opendatasets.download('https://www.kaggle.com/datasets/rmisra/news-category-dataset')

# Open dataset
data = []
with open('news-category-dataset/News_Category_Dataset_v3.json', 'r') as file:

  # Iterate through the lines of the JSON file
  for line in file.readlines():

    # Convert line into a python dictionaries
    article = json.loads(line)
  
    # Format data
    document = {
      "title": article['headline'],
      "teaser": article['short_description'],
      "url": article['link'],
      "content_type": "article",
      "portal": "HuffPost",
      "rubrik": article['category'],
      "created": article['date']
    }

    data.append(document)


# Add articles to the database via the API
# Hint: Make sure the ORB ist running on http://localhost:8000
r = requests.post('http://localhost:8000/article/', json=data)

print(f"Finished: Added {len(data)}/{len(data)} articles")