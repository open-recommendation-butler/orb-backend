# How to add the News Category Dataset to the database?

This tutorial shows you how to add a full dataset to the database. We use a small Python script and the News Category Dataset.

## About the dataset

The [News Category Dataset](https://www.kaggle.com/datasets/rmisra/news-category-dataset) contains around 210k news headlines and teasers from 2012 to 2022 from HuffPost. 

It is a good use case to test ORB.

Each record in the dataset consists of the following attributes:
- category: category in which the article was published.
- headline: the headline of the news article.
- authors: list of authors who contributed to the article.
- link: link to the original news article.
- short_description: Abstract of the news article.
- date: publication date of the article.

We will add those attributes to the database.

## Requirements

* ORB is up and running. See: [How to get started](https://github.com/open-recommendation-butler/ORB#how-to-get-started)
* A kaggle account. It's free: [Register at Kaggle](https://www.kaggle.com/)
* An API key from Kaggle. More information: [Kaggle's documentation for authentication](https://www.kaggle.com/docs/api#authentication)
* The opendatasets and requests libraries. You can install them with the following command:

```bash
pip install requests opendatasets
```

## Run the code

To download the dataset from Kaggle and to insert it into the dataset, you can use this script: [adding-news-category-dataset.py](/tutorials/adding-news-category-dataset/adding-news-category-dataset.py)

You can run the script from the main directory with the following command:

```bash
python tutorials/adding-news-category-dataset/adding-news-category-dataset.py
```

ORB will convert the articles to embeddings and index them. Depending on your machine, this might take up some hours.
