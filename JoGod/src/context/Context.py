from api.RestaurantResource import RestaurantResource
from api.SegmentResource import SegmentResource
from config import Config
from api.HeartbeatResource import HeartbeatResource
from infrastructure.restaurant.MongoRestaurantRepository import (
    MongoRestaurantRepository,
)
from infrastructure.segment.MongoSegmentRepository import MongoSegmentRepository
from server.ApplicationServer import ApplicationServer


class Context:
    def __init__(self):
        self.__application_server = self.__create_application_server()

    def run(self):
        self.__application_server.run(Config.BASE_HOSTNAME)

    def __create_application_server(self) -> ApplicationServer:
        heartbeat_resource = HeartbeatResource(Config.CHOSEN_CITY)
        restaurant_resource = self.__create_restaurant_resource()
        segment_resource = self.__create_segment_resource()

        return ApplicationServer(heartbeat_resource, restaurant_resource, segment_resource)

    def __create_restaurant_resource(self) -> RestaurantResource:
        restaurant_repository = MongoRestaurantRepository(Config.MONGO_ADDRESS)
        return RestaurantResource(restaurant_repository)

    def __create_segment_resource(self) -> SegmentResource:
        segment_repository = MongoSegmentRepository(Config.MONGO_ADDRESS)
        return SegmentResource(segment_repository)
