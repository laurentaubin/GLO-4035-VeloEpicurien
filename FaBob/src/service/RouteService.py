from domain.graph.GraphRepository import GraphRepository
from domain.restaurant.RestaurantRepository import RestaurantRepository


class RouteService:
    def __init__(self, restaurant_repository: RestaurantRepository, graph_repository: GraphRepository):
        self.__restaurant_repository = restaurant_repository
        self.__graph_repository = graph_repository

    def generate_route(self):
        self.__graph_repository.generate_route()


    def get_vertex_starting_point(self, latitude: float, longitude: float):
        return {}
        # vertex_starting_point = self.get_vertex_starting_point(latitude, longitude)
        # return vertex_starting_point