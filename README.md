# Velo epicurien

## App structure
### Services
| Name  | Description        |
|-------|-------------|
| [JoGod](JoGod) | Python Api Gateway |
| [FaBob](FaBob) | Python data transformer and sink to MongoDB |
| [Thierry](Thierry) | Python scripts to extract raw data from external APIs |

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

## Contributors
- Laurent Aubin
- Toma Gagné
- Maxime Nasso
