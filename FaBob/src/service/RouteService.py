from domain.graph.GraphRepository import GraphRepository
from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.route.RouteRepository import RouteRepository


class RouteService:
    def __init__(
        self,
        restaurant_repository: RestaurantRepository,
        graph_repository: GraphRepository,
        route_repository: RouteRepository,
    ):
        self.__restaurant_repository = restaurant_repository
        self.__graph_repository = graph_repository
        self.__route_repository = route_repository

    def generate_route(self):
        generated_routes = self.__graph_repository.generate_routes_resto_to_resto()
        self.__route_repository.save_routes(generated_routes)

    def get_vertex_starting_point(self, latitude: float, longitude: float):
        return {}
        # vertex_starting_point = self.get_vertex_starting_point(latitude, longitude)
        # return vertex_starting_point
