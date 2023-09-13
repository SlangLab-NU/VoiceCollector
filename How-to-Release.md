# This document explains the release process for voice collector on Amazon EC2

## Building release docker images
1. Create a new branch based on the lastest dev branch. Name the new branch release-[veriosn], for example you can name the branch release-1.3.4
2. Edit the version numbers and image names as necessary in `docker-compose.prod.yml` docker compose file.
3. Run `docker-compose -f docker-compose.prod.yml build` on your development machine to build the release image.
4. Run `docker-compose -f docker-compose.prod.yml push` on your development machine to push the release image to dockerhub. It is necessary you build and push it on your dev machine because building the image is quite computational expensive. Note this also assume you have a dockerhub account and have setup the account on your machine. If not, please go to dockerhub and create an Access Token on your dev machine.

## Deploying release on Amazon EC2



### Obtain certificate initially using certbot

``` bash
docker-compose -f docker-compose.prod.yml up web
```
``` bash
docker-compose -f docker-compose.prod.yml run --entrypoint "certbot" certbot certonly --webroot --webroot-path=/var/www/certbot --email admin@happyprime.io --agree-tos --no-eff-email -d voicecollector.happyprime.io
```