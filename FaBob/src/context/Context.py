import http.client
import json
import time

import requests

from api.LoaderResource import LoaderResource
from config import Config
from domain.route.RouteRepository import RouteRepository
from infrastructure.graph.NeoGraphRepository import NeoGraphRepository
from infrastructure.restaurant.MongoRestaurantRepository import (
    MongoRestaurantRepository,
)
from infrastructure.route.MongoRouteRepository import MongoRouteRepository
from infrastructure.segment.MongoSegmentRepository import MongoSegmentRepository
from server.ApplicationServer import ApplicationServer
from service.ConnectorService import ConnectorService
from service.RouteService import RouteService


class Context:
    def __init__(self):
        self.__application_server = self.__create_application_server()

    def run(self):
        restaurant_repository = MongoRestaurantRepository(
            Config.MONGO_ADDRESS, Config.RESTAURANTS_FILE_PATH
        )
        segment_repository = MongoSegmentRepository(
            Config.MONGO_ADDRESS,
            Config.SEGMENTS_FILE_PATH,
        )

        loader_resource = LoaderResource(restaurant_repository, segment_repository)
        loader_resource.load_segments()
        loader_resource.load_restaurants()
        connector_service = ConnectorService(
            restaurant_repository, segment_repository
        )

        connector_service.connect_near_restaurants_to_segments()
        self.__send_load_segment_beaubrun()

        graph_repository = NeoGraphRepository(
            Config.NEO4J_CONNECTION_HOST, Config.NEO4J_PORT
        )
        route_repository = MongoRouteRepository(Config.MONGO_ADDRESS)

        route_service = RouteService(
            restaurant_repository, graph_repository, route_repository
        )
        route_service.generate_route()
        self.__application_server.run("0.0.0.0")

    def __create_application_server(self) -> ApplicationServer:
        return ApplicationServer()

    def __send_load_segment_beaubrun(self):
        while True:
            try:
                requests.post("http://beaubrun:5000/load_segments")
                return
            except Exception as err:
                print("\nERROR WHILE SENDING REQUEST TO BEAUBRUN: {0}\n".format(err))
                time.sleep(2)
