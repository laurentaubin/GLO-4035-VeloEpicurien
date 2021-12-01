from service.RouteService import RouteService


class RouteResource:
    def __init__(self, route_service: RouteService):
        self.__route_service = route_service
