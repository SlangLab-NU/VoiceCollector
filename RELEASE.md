# **Application Deployment Guide**

This guide provides a comprehensive overview of setting up, developing, and releasing our application using Docker and deploying it on Amazon EC2.

## **Docker Instructions for Development and Testing**

### **Installing and Starting Docker Desktop**

1. Install Docker Desktop by following this link: [Docker Desktop](https://www.docker.com/).
2. Run Docker Desktop and sign in.

### **Building Docker Images**

From the root directory, where the three Dockerfiles (`Dockerfile.minio`, `Dockerfile.server`, and `Dockerfile.web`) are located:

```
docker build -f ./dockerfiles/Dockerfile.minio -t minio .
docker build -f ./dockerfiles/Dockerfile.server -t server .
docker build -f ./dockerfiles/Dockerfile.web -t web .
```

### **Running the Application**

1. Modify `REACT_APP_API_URL` and `REACT_APP_PORT_NUMBER` in the `docker-compose.dev.yml` and `docker-compose.prod.yml` files as needed.
2. Ensure `REACT_APP_API_URL` is served via HTTPS or accessed via localhost.
Note: For REACT_APP_API_URL, you have to serve it via https or access the api via localhost otherwise the service will not work.
3. Use docker-compose to run the containers:
   - For development (Flask): `docker-compose -f docker-compose.dev.yml up -d`
   - For production (Gunicorn): `docker-compose -f docker-compose.prod.yml up -d`
   - Note: The -d flag can be omitted if you want to view the logs from the command line console. The logs can also be viewed from the Docker Desktop app.
4. Access the app at http://localhost:3000.
5. For a combined build and run command, add the `--build` flag.

### **Stopping the Application**

```
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.prod.yml down
```

### **Running Containers Separately**

- MinIO: `docker run --rm -p 9000:9000 minio`
- Server (Development): `docker run --rm -p 5000:5000 --env FLASK_APP=__init__ server flask run --host=0.0.0.0`
- Server (Production): `docker run --rm -p 5000:5000 --workdir /server server gunicorn -w 4 --bind 0.0.0.0:5000 app:application`

For frontend, navigate to the `web` directory and use `yarn start`.

## **Release Process for Voice Collector on Amazon EC2**

### Building release docker images
1. Create a new branch based on the lastest release branch. Name the new branch release-[veriosn], for example you can name the branch release-1.3.4. Then merge the lastest code from dev branch.
2. Edit the version numbers and image names as necessary in `docker-compose.prod.yml` docker compose file. For example you may want to tag the docker image a higher version number based on the changes in the code.
3. Run `docker-compose -f docker-compose.prod.yml build` on your development machine to build the release image.
4. Run `docker-compose -f docker-compose.prod.yml push` on your development machine to push the release image to dockerhub. It is necessary you build and push it on your dev machine because building the image is quite computational expensive. Note this also assume you have a dockerhub account and have setup the account on your machine. If not, please go to dockerhub and create an Access Token on your dev machine.

### Making sure docker and git is available in EC2

Most of time docker and docker-compose is not available in EC2 and you need to install it yourself. Also sometimes git is not available. Please make sure they are installed.

### Obtaining certificate initially using certbot
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


## Generate a CSV File from VoiceCollector Data

To generate a CSV file containing paths to audio files and their corresponding transcriptions from the VoiceCollector data, follow these steps. 

### Prerequisites:

1. SSH access to the cloud server where VoiceCollector is running.
2. Docker installed on the server.
3. Ensure that there is at least one audio file submitted to the VoiceCollector system.

### Steps

- SSH into the Cloud Server

- Compile Docker: Ensure that Docker is installed on the cloud server. 

- API Request via CLI
``` bash
curl -X GET http://localhost:5000/api/v1/speak/get_csv
```

- After accessing the endpoint, you will receive a response similar to the following:
```
{"csv_path":"/tmp/output.csv","message":"CSV file generation complete"}
```
Saved file will be stored in local folder `data/voice/output` 
