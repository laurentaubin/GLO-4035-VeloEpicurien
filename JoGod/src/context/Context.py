from api.ExtractedDataResource import ExtractedDataResource
from api.HeartbeatResource import HeartbeatResource
from api.ReadMeResource import ReadMeResource
from api.RouteResource import RouteResource
from api.TransformedDataResource import TransformedDataResource
from config import Config
from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.SegmentRepository import SegmentRepository
from infrastructure.graph.NeoGraphRepository import NeoGraphRepository
from infrastructure.restaurant.MongoRestaurantRepository import (
    MongoRestaurantRepository,
)
from infrastructure.route.MongoRouteRepository import MongoRouteRepository
from infrastructure.segment.MongoSegmentRepository import MongoSegmentRepository
from server.ApplicationServer import ApplicationServer
from service.RouteService import RouteService


class Context:
    def __init__(self):
        self.__application_server = self.__create_application_server()

    def run(self):
        self.__application_server.run(Config.BASE_HOSTNAME)

    def __create_application_server(self) -> ApplicationServer:
        segment_repository = MongoSegmentRepository(Config.MONGO_ADDRESS)
        restaurant_repository = MongoRestaurantRepository(Config.MONGO_ADDRESS)
        graph_repository = NeoGraphRepository(
            Config.NEO4J_CONNECTION_HOST, Config.NEO4J_PORT
        )

        heartbeat_resource = HeartbeatResource(Config.CHOSEN_CITY)
        readme_resource = ReadMeResource(Config.README_PATH)
        transformed_data_resource = self.__create_transformed_data_resource(
            segment_repository, restaurant_repository
        )
        extracted_data_resource = self.__create_extracted_data_resource(
            segment_repository, restaurant_repository
        )

        route_repository = MongoRouteRepository(Config.MONGO_ADDRESS)

        route_service = RouteService(
            restaurant_repository, graph_repository, route_repository
        )
        route_resource = RouteResource(route_service, restaurant_repository)

        return ApplicationServer(
            heartbeat_resource,
            readme_resource,
            extracted_data_resource,
            transformed_data_resource,
            route_resource,
        )

    def __create_transformed_data_resource(
        self,
        segment_repository: SegmentRepository,
        restaurant_repository: RestaurantRepository,
    ) -> TransformedDataResource:
        return TransformedDataResource(segment_repository, restaurant_repository)

    def __create_extracted_data_resource(
        self,
        segment_repository: SegmentRepository,
        restaurant_repository: RestaurantRepository,
    ) -> ExtractedDataResource:
        return ExtractedDataResource(segment_repository, restaurant_repository)
