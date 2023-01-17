# How to deploy Open Recommendation Butler on a server?

Open Recommendation Butler comes prepared for deployment. For deployment, we use NGINX and Gunicorn. Both come ready configured with this repository. We will user docker-compose.prod.yml instead of docker-compose.yml to set up the Docker.

## Requirements

You need a deployment server with Docker and Git installed and root rights. Optionally, you need a registered domain. Alternativelly, you can access ORB via the IP adress of your server.

## Setting up the docker

1. Clone the repository

```bash
git clone https://github.com/open-recommendation-butler/ORB.git
```

2. Change directory to project directory

```bash
cd ORB
```

3. Create a file with the name ".env".

4. Insert the following content into the ".env" file. Replace *YourStrongPasswordForElasticSearch*, *YourStrongPasswordForKibana* and *YourStrongSecretKeyForDjango* with your own passwords. Replace *example.org* with your domain or IP adress.

Content of ".env" file:
```bash
# Password for the 'elastic' user (at least 6 characters)
ELASTIC_PASSWORD=YourStrongPasswordForElasticSearch

# Password for the 'kibana_system' user (at least 6 characters)
KIBANA_PASSWORD=YourStrongPasswordForKibana

# Secret key for Django (at least 6 characters)
SECRET_KEY=YourStrongSecretKeyForDjango

# Turn off Django's debug mode. Having DEBUG=True in deployment, is a security risk.
DEBUG=False

# The domain for ORB. Alternatively, this can be an IP adress. 
DOMAIN=example.com
```

5. Compose the docker
```bash
docker compose -f docker-compose.prod.yml build
```

6. Compose the docker
```bash
docker compose -f docker-compose.prod.yml up -d
```

7. Test if ORB is running by visiting your domain or IP adress.


## *Optionally:* Securing ORB with SSL

You can secure the access to ORB with SSL. To do so, we will create a certificate with [Let's encrypt](https://letsencrypt.org/) and [certbot](https://certbot.eff.org/).

To do so, run the following command on the server. Remember to replace *YourMailAdress* and *YourDomain*. It's recommended to use a working mail adress. You will receive a notification if your certificate expires. 

```bash
docker exec orb-nginx-1 certbot --nginx -n --agree-tos -m YourMailAdress -d YourDomain
```

Hint: This certificate will expire after 3 months. To set an auto renewal, set a cronjob inside the orb-nginx-1 container:

```
0 0 1 * * certbot renew --quiet
```
