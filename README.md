# Open Recommendation Butler (ORB)
ORB helps news readers to find information faster by developing an open source toolbox knowledge-based thematic recommendations and search results.


This is a django wrapper around an ElasticSearch engine. It's optimized for publishers.

-> See the full [ORB on Github](https://github.com/open-recommendation-butler)

## How to get started

You can start ORB on your machine with docker by following these steps.

1. Clone the repository

```bash
git clone https://github.com/open-recommendation-butler/ORB.git
```

2. Change directory to project directory

```bash
cd ORB
```

3. Create a file with the name ".env".

4. Insert the following content into the ".env" file. Replace YourStrongPasswordForElasticSearch, YourStrongPasswordForKibana and YourStrongSecretKeyForDjango with your own passwords.

Content of ".env" file:
```bash
# Password for the 'elastic' user (at least 6 characters)
ELASTIC_PASSWORD=YourStrongPasswordForElasticSearch

# Password for the 'kibana_system' user (at least 6 characters)
KIBANA_PASSWORD=YourStrongPasswordForKibana

# Secret key for Django (at least 6 characters)
SECRET_KEY=YourStrongSecretKeyForDjango
```

5. Compose the docker
```bash
docker compose build
```

6. Compose the docker
```bash
docker compose up -d
```

7. Test if ORB is running by visiting [http://localhost:8000](http://localhost:8000).

## Tutorials

[1. How to add documents to the database?](../main/tutorials/1-adding-documents-to-the-database/adding-documents-to-the-database.md)

[2. How to search for documents with the API?](../main/tutorials/2-searching-for-documents/searching-for-documents.md)

[3. How to add the News Category Dataset to the database?](../main/tutorials/adding-news-category-dataset/addingg-news-category-dataset.md)

[4. How to deploy on a production server?](../main/tutorials/4-deploy-orb/deploy-orb.md)

## Supported by

Media Tech Lab [`media-tech-lab`](https://github.com/media-tech-lab)

<a href="https://www.media-lab.de/en/programs/media-tech-lab">
    <img src="https://raw.githubusercontent.com/media-tech-lab/.github/main/assets/mtl-powered-by.png" width="240" title="Media Tech Lab powered by logo">
</a>
