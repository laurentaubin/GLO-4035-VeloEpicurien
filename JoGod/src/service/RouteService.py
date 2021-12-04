from typing import List

from domain.graph.GraphRepository import GraphRepository
from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.route.RouteRepository import RouteRepository


class RouteService:
    def __init__(
            self,
            restaurant_repository: RestaurantRepository,
            graph_repository: GraphRepository,
            route_repository: RouteRepository
    ):
        self.__restaurant_repository = restaurant_repository
        self.__graph_repository = graph_repository
        self.__route_repository = route_repository

    def find_starting_point(self, length: int, types: List[str]):
        return {
            "startingPoint": self.__route_repository.find_starting_point(length, types)["geometry"]}

    def generate_route(
            self, starting_point: dict, types: List[str], number_of_stops: int, length: int
    ):
        return self.__route_repository.find_route(starting_point, types, length, number_of_stops)

    def add_types_to_routes(self):
        self.__route_repository.add_types()
