from typing import List

from flask import request
from service.RouteService import RouteService


class RouteResource:
    def __init__(self, route_service: RouteService):
        self.__route_service = route_service

    def find_starting_point(self, request) -> dict:
        body = request.get_json()
        if not body:
            return {"error": "bad request", "description": "missing body"}
        print(body["length"])
        length: int = int(body["length"])
        desired_types: List[str] = body["type"]

        return self.__route_service.find_starting_point(length, desired_types)





    def generate_route(self, request):
        body = request.get_json()
        if not body:
            return {"error": "bad request", "description": "missing body"}

        starting_point: dict = body["startingPoint"]
        restaurant_types: List[str] = body["type"]
        number_of_stops: int = body["numberOfStops"]
        length: int = body["length"]

        return self.__route_service.generate_route(
            starting_point, restaurant_types, number_of_stops, length
        )
