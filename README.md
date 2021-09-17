# Velo epicurien - Name TBD

## App structure
### Services
| Name  | Role        |
|-------|-------------|
| JoGod | Api Gateway |

## Getting started
Follow these instructions to get a copy of the project up and running on your local machine

### Run the app locally using Docker
Make sure you have the latest versions of [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

build the app:
```bash
docker-compose build
```

run the app:
```bash
docker-compose up
```

Additionally, you can do both at the same time:
```bash
docker-compose up --build
```