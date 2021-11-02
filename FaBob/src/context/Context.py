from api.LoaderResource import LoaderResource
from config import Config
from infrastructure.restaurant.MongoRestaurantRepository import (
    MongoRestaurantRepository,
)
from infrastructure.segment.MongoSegmentRepository import MongoSegmentRepository
from server.ApplicationServer import ApplicationServer


class Context:
    def __init__(self):
        self.__application_server = self.__create_application_server()

    def run(self):
        loader_resource = LoaderResource(
            MongoRestaurantRepository(
                Config.MONGO_ADDRESS, Config.RESTAURANTS_FILE_PATH
            ),
            MongoSegmentRepository(
                Config.MONGO_ADDRESS,
                Config.SEGMENTS_FILE_PATH,
            ),
        )
        loader_resource.load_segments()
        loader_resource.load_restaurants()
        self.__application_server.run("0.0.0.0")

    def __create_application_server(self) -> ApplicationServer:
        return ApplicationServer()
