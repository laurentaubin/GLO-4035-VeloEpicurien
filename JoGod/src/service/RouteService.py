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
            "starting_point": self.__route_repository.find_starting_point(length, types)["geometry"]}

    def generate_route(
            self, starting_point: dict, type: List[str], number_of_stops: int, length: int
    ):
        starting_vertex_node = self.__graph_repository.get_starting_vertex_node(
            starting_point
        )

        pass
