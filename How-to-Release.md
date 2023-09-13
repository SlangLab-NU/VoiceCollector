# This document explains the release process for voice collector on Amazon EC2

## Building release docker images
1. Create a new branch based on the lastest release branch. Name the new branch release-[veriosn], for example you can name the branch release-1.3.4. Then merge the lastest code from dev branch.
2. Edit the version numbers and image names as necessary in `docker-compose.prod.yml` docker compose file. For example you may want to tag the docker image a higher version number based on the changes in the code.
3. Run `docker-compose -f docker-compose.prod.yml build` on your development machine to build the release image.
4. Run `docker-compose -f docker-compose.prod.yml push` on your development machine to push the release image to dockerhub. It is necessary you build and push it on your dev machine because building the image is quite computational expensive. Note this also assume you have a dockerhub account and have setup the account on your machine. If not, please go to dockerhub and create an Access Token on your dev machine.

## Deploying release on Amazon EC2

### Make sure docker and git is available in EC2

Most of time docker and docker-compose is not available in EC2 and you need to install it yourself. Also sometimes git is not available. Please make sure they are installed.

### Obtain certificate initially using certbot
If this is a brand new instance or you just changed your domain, you need to obtain your first ssl certificate from letencrypt. This step can be skipped if you already have a valid ssl certificate on your instance.
1. Take a look at nginx.prod.conf and nginx.init.conf. Make sure `server_name` and `ssl_certificate` are set to appropreiate values. 
2. During initial chanllenge validation, we need to setup a plain http host on port 80. Edit web service in `docker-compose.prod.yml` file so it use a simple init nginx config:
``` yml
web:
    ...
    volumes:
        - ...
        - ./dockerfiles/nginx.init.conf:/etc/nginx/conf.d/default.conf
```
3. bring web container up. Check the log that nginx is serving without issue.
``` bash
docker-compose -f docker-compose.prod.yml up web
```
4. Run certbot container to grab initial certificate:
``` bash
docker-compose -f docker-compose.prod.yml run --entrypoint "certbot" certbot certonly --webroot --webroot-path=/var/www/certbot --email admin@happyprime.io --agree-tos --no-eff-email -d voicecollector.happyprime.io
```
Note letsencrypt limit the number of certificates you can grab from it in a period of time. So if you are not sure if your command is going to work it is best to test on the staging server:
``` bash
docker-compose -f docker-compose.prod.yml run --entrypoint "certbot" certbot certonly --webroot --webroot-path=/var/www/certbot --email admin@happyprime.io --agree-tos --no-eff-email -d voicecollector.happyprime.io --staging
```
5. If everything is going smooth, certbot should tell you that you have obtain the certificates successfully and they are stored in data/certbot folder. Web server should see a few request from certbot during the challenge process. **Never** upload the content of data folder to github for security reasons.

### Spining up the service
Now you have the certificate stored, shutdown and remove exisiting containers. Change the content of docker-compose.prod.yml back to production config:
``` yml
web:
    ...
    volumes:
        - ...
        - ./dockerfiles/nginx.prod.conf:/etc/nginx/conf.d/default.conf
```
and spin up the service by running:
``` bash
docker-compose -f docker-compose.prod.yml up -d
```
verify the service is working by testing the web app and examine the logs in realtime:
``` bash
docker-compose -f docker-compose.prod.yml logs -f
```