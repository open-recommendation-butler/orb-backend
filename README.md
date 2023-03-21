# Open Recommendation Butler - Find what feels missing
Good search is complex to implement. Every day media houses loose traffic to Google. This open source project is an easy to implement state of the art AI powered search engine for media houses.

<a href="https://github.com/open-recommendation-butler"> 🏠 Project side</a>: Learn more about the project

<a href="https://open-recommendation-butler.tech/"> 🌐 Demo</a>: Check out the power

<a href="https://open-recommendation-butler.github.io/orb-docs/">📑 Docs</a>: Get started in a few minutes

<img src="https://user-images.githubusercontent.com/40501887/221694829-5e90816f-f723-45cc-8409-ccee7ba90860.jpg" width="750" title="Screenshot of Open Recommendation Butler showing its functionality">

## How to get started

You can start ORB on your machine with docker by following these steps:

- Clone the repository

```bash
git clone https://github.com/open-recommendation-butler/ORB.git
```

- Change directory to project directory

```bash
cd ORB
```

- Create a file with the name ".env".

- Insert the following content into the ".env" file. Replace *YourStrongPasswordForElasticSearch*, *YourStrongPasswordForKibana* and *YourStrongSecretKeyForDjango* with your own passwords.

```bash
# Content of ".env" file:

# Password for the 'elastic' user (at least 6 characters)
ELASTIC_PASSWORD=YourStrongPasswordForElasticSearch

# Password for the 'kibana_system' user (at least 6 characters)
KIBANA_PASSWORD=YourStrongPasswordForKibana

# Secret key for Django (at least 6 characters)
SECRET_KEY=YourStrongSecretKeyForDjango
```

- Compose the docker
```bash
docker compose build
```

- Compose the docker
```bash
docker compose up -d
```

- Test if ORB is running by visiting [http://localhost:8000](http://localhost:8000).

<a href="https://open-recommendation-butler.github.io/Docs/">For more see full documentation here.</a>

## Sponsors

This project is kindly funded and supported by:

<a href="https://media-tech-lab.com">Media Tech Lab by Media Lab Bayern</a> (<a href="https://github.com/media-tech-lab">@media-tech-lab</a>)

<a href="https://media-tech-lab.com">
    <img src="https://github.com/media-tech-lab/.github/blob/main/assets/mtl-powered-by.png" width="240" title="Media Tech Lab powered by logo">
</a>
