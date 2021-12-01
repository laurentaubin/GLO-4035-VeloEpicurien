from typing import List

from flask import request
from service.RouteService import RouteService


class RouteResource:
    def __init__(self, route_service: RouteService):
        self.__route_service = route_service

    def generate_route(self, request):
        body = request.get_json()
        if not body:
            return {"error": "bad request", "description": "missing body"}

        starting_point: dict = body["startingPoint"]
        type: List[str] = body["type"]
        number_of_stops: int = body["numberOfStops"]

        self.__route_service.generate_route()

