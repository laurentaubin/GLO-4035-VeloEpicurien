from typing import List

from domain.graph.GraphRepository import GraphRepository
from domain.restaurant.RestaurantRepository import RestaurantRepository


class RouteService:
    def __init__(self, restaurant_repository: RestaurantRepository, graph_repository: GraphRepository):
        self.__restaurant_repository = restaurant_repository
        self.__graph_repository = graph_repository

    def generate_route(self, starting_point: dict, type: List[str], number_of_stops: int, length: int):
        pass
