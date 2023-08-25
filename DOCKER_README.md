# Docker Instructions

This is a step-by-step instructions for installing Docker Desktop, building Docker images for our application components, and running the application containers.

## Installing and Starting Docker Desktop

1. Install Docker Desktop by following this link: [Docker Desktop](https://www.docker.com/).

2. Run Docker Desktop and sign in.

## Building the Docker Images

From the root directory, where the three Dockerfiles (`Dockerfile.minio`, `Dockerfile.server`, and `Dockerfile.web`) are located, build the Docker images using the following commands:

```
docker build -f Dockerfile.minio -t minio .
docker build -f Dockerfile.server -t server .
docker build -f Dockerfile.web -t web .
```

## Running the Application

Use docker-compose to build and run the containers simultaneously:
`docker-compose up -d`

- The -d flag can be omitted if you want to view the logs from the command line console. The logs can also be viewed from the Docker Desktop app.

- Access the app at http://localhost:3000.

## Stopping the Application

To stop the containers, run the following command:
`docker-compose down`

## Running Container Separately

Alternatively, the MinIO and Server containers can be ran separately:

1. Run MinIO docker:
   `docker run --rm -p 9000:9000 minio`

2. Run server docker:
   `docker run --rm -p 5000:5000 server`

Please note that the container for the frontend can only be run using docker-compose. If you want to run the frontend separately, navigate to the `web` directory and use:
`yarn start`.
