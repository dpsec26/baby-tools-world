# Baby Tools World

This repository contains the source code of the 'Baby Tools World' which is a simple full stack shop application written in Python using Django 6.
The project was developed for educational purposes only and therefore has no claim to feature completeness, or only minimal claims regarding application security, user experience, or design.

## Features

### Product tags

Products can be tagged with labels (e.g. "New", "Promotion"). Tags are shown on the product details page.
All tags can be managed in the Django admin panel. Multiple tags are supported.

## Prerequisites

- Docker Engine or Docker Desktop
- Editor/IDE of your choice

## Quickstart

In order to quickly get started with the project follow these steps:

1. clone the repository
1. navigate to the repository
1. configure required application environment variables
    1. `cp example.env src/.env`
    1. edit the src/.env file
1. build the docker image
    - `docker build -t baby-tools-world:local .`
1. run the docker container
    - `docker run -d -p 8000:8000 --name baby-tools-world baby-tools-world:local`
1. setup superuser and fill the database with test data
    1. `docker exec -it baby-tools-world sh`
    1. `python manage.py createsuperuser`
    1. (optional) `python manage.py seed_db`
1. verify the application is running by visiting `localhost:8000`

## Usage

### Configuration

To configure the project, follow these steps:

1. Copy the example environment file to the `src` directory: `cp example.env src/.env`.
    - the file needs to be stored next to the manage.py file in order to function properly. 
    Other locations might also work but there is no guarantee, and in last consequence you will need to update to project correspondingly.
2. Open your `src/.env` and set the required environment variables:
    - `ALLOWED_HOSTS`: provide a list of comma-separated values for the allowed host configuration => Defaults to `'localhost, 127.0.0.1, 0.0.0.0'`
    - `AUTHOR`: Set it to your name.
    - `DEBUG`: Set to `True` for development or `False` for production. Defaults to `True`

### Containerization

#### Build the image

You can build the container image by running the following command in your terminal:

```sh
# use -t to provide a tag together with the image name
# -> baby-tools-world is the image name, 'local' is the tag
docker build -t baby-tools-world:local .
```

#### Run the container

> [!IMPORTANT]
> If you are using Windows, you have to convert `CRLF` to `LF` in the `entrypoint.sh`. Otherwise the application will not run. You can do this in an editor or use a tool like `dos2unix`.
> If you run the container detached `-d`, you won't see that the application did not start.

To start a container based on the image, use the following command in your terminal:

```sh
docker run -d -p 8000:8000 --name baby-tools-world baby-tools-world:local
```
> [!NOTE]
> You should `--name` the container, so you can access the interactive terminal with `docker exec -it <container-name> sh`

#### Access the running container

If your container has a name, you can access an interactive terminal with:
```sh
docker exec -it baby-tools-world sh
```
This terminal lets you run commands inside the container. You will need this to create an admin user and seed the application with test data.
Exit the terminal with `exit`.

### Setup a superuser

[Access the running container](#access-the-running-container) and run the management command
```sh
python manage.py createsuperuser
```
in order to create your admin user.

### Seed the application with test data

[Access the running container](#access-the-running-container) and run the management command
```sh
python manage.py seed_db
```
A few test products will be created in the database.
