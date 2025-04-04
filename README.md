
# Local Dev Setup

## Python / Poetry Setup

I'll add more details soon but to get started:

follow poetry install instructions [here](https://python-poetry.org/docs/#installation)

`cd pricing-service`

### install packages

`poetry install`

### enter poetry shell

`poetry shell`

### start webapp:

`python run src/main/python/webapp.py`

# Docker Setup

## Docker Build

` docker build -f docker/Dockerfile -t pricing-service .`

## Docker Run

`docker run -p 8081:80 -it pricing-service`

after starting docker, browse to http://localhost:8081/docs to see app endpoints
