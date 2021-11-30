from api.LoaderResource import LoaderResource
from config import Config
from infrastructure.graph.NeoGraphRepository import NeoGraphRepository
from infrastructure.restaurant.MongoRestaurantRepository import (
    MongoRestaurantRepository,
)
from infrastructure.segment.MongoSegmentRepository import MongoSegmentRepository
from server.ApplicationServer import ApplicationServer
from service.GraphService import GraphService


class Context:
    def __init__(self):
        self.__application_server = self.__create_application_server()

    def run(self):
        self.__application_server.run("0.0.0.0")

    def __create_application_server(self) -> ApplicationServer:
        restaurant_repository = MongoRestaurantRepository(
            Config.MONGO_ADDRESS
        )
        segment_repository = MongoSegmentRepository(Config.MONGO_ADDRESS)
        graph_repository = NeoGraphRepository(Config.NEO4J_CONNECTION_HOST, Config.NEO4J_PORT)

        graph_service = GraphService(graph_repository, segment_repository, restaurant_repository)

        loader_resource = LoaderResource(
            graph_service
        )
        return ApplicationServer(loader_resource)
