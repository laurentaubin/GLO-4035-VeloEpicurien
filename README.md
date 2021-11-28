# Velo epicurien

## App structure
### Services
| Name  | Description        |
|-------|-------------|
| [JoGod](JoGod) | Python Api Gateway |
| [FaBob](FaBob) | Python data transformer and sink to MongoDB |
| [Thierry](Thierry) | Python scripts to extract raw data from external APIs |

## Getting started
Follow these instructions to get a copy of the project up and running on your local machine.

Make sure you have the latest versions of [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

### Using startup script
Run `./start.sh`

### Run the app manually using Docker

Copy the README.md file:
```bash
cp README.md JoGod/PROJECT_README/md
```

Build the app:
```bash
docker-compose build
```

Run the app:
```bash
docker-compose up
```

Additionally, you can do the last two steps at the same time:
```bash
docker-compose up --build
```

## Using the application
Once started, a web server runs locally on port 80. 

### Available routes

#### Readme
Returns this file
```
@GET /readme
```

#### Heartbeat
Returns the city used for the app.
```
@GET /heartbeat

returns:
{
    "villeChoisie": str
}
```

#### Extracted data
Returns information about the raw data used in the app
```
@GET /extracted_data

returns:
{
    "nbRestaurants":int,
    "nbSegments":int
}
```

#### Transformed data
Returns information about the data used in the app once it has been processed
```
@GET /transformed_data

returns:
{
    "restaurants":{
        $type1: int,
        $type2: int,
        ...
    },
    "longueurCyclable":float
}
```

#### Restaurant types
Returns the list of all available restaurant types

```
@GET /type

returns:
[
    str,
    str,
    str,
    ...
]
```

#### Get a starting point
Generates the starting point of a random route of length `length` (± 10%) and containing restaurants of types in `type`. All restaurant types will be considered if `type` is an empty array.

```
@GET /starting_point:
{
    "length": int (en mètre),
    "type": [str, str, ... ]
}

returns:
{
    "startingPoint" : {"type":"Point", "coordinates":[float, float]}
}
```

#### Generate a route
Generates a route of length `length` (± 10%) starting within 500 meters of `startingPoint` with at most `numberOfStops` stops at restaurants of types in `type`. All restaurant types will be considered if `type` is an empty array. 

```
@GET /parcours (avec le payload):
{
    "startingPoint" : {"type":"Point", "coordinates":[float, float]},
    "length": int (en mètre),
    "numberOfStops": int,
    "type": [str, str, ... ]
}

returns:
{
    "type": "FeatureCollection",
    "features": [
        {
            "type":"Feature",
            "geometry":{
                "type": "Point",
                "coordinates":  [float, float]
            },
            "properties":{
                "name":str,
                "type":str
            }
        }, ..., {
            "type":"Feature",
            "geometry":{
                "type": "MultiLineString",
                "coordinates": [[
                     [float, float],  [float, float],  [float, float], ...
                    ]]
            },
            "properties":{
                "length":float (en mètres)
            }
        }
    ]
}
```

## Contributors
- Laurent Aubin
- Toma Gagné
- Maxime Nasso
