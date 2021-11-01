from api.LoaderResource import LoaderResource
from infrastructure.restaurant.MongoRestaurantRepository import (
    MongoRestaurantRepository,
)
from infrastructure.segment.MongoSegmentRepository import MongoSegmentRepository
from server.ApplicationServer import ApplicationServer


class Context:
    def __init__(self):
        self.__application_server = self.__create_application_server()

    def run(self):
        self.__application_server.run("0.0.0.0")

    def __create_application_server(self) -> ApplicationServer:
        return ApplicationServer(
            LoaderResource(
                MongoRestaurantRepository(
                    "mongodb://mongodb_epicurien:27017", "src/data/restaurant_data.json"
                ),
                MongoSegmentRepository(
                    "mongodb://mongodb_epicurien:27017",
                    "src/data/vdq-reseaucyclable.json",
                ),
            )
        )
