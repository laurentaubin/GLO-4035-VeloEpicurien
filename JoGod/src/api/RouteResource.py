from typing import List

from flask import request, make_response
from service.RouteService import RouteService

from jsonschema import validate


class RouteResource:
    def __init__(self, route_service: RouteService):
        self.__route_service = route_service

    def find_starting_point(self, request):
        body = request.get_json()
        if not body:
            return make_response("bad request", 400)

        if "length" not in body or "type" not in body:
            return make_response("missing length or/and type", 400)

        if not isinstance(body["length"], int):
            return make_response("length must be an integer", 400)

        for desired_type in body["type"]:
            if not isinstance(desired_type, str):
                return make_response("type must be an array of strings", 400)

        schema = {
            "type": "object",
            "properties": {
                "type": {"type": "array"}
            },
        }

        try:
            validate(body, schema)
        except Exception:
            return make_response("type must be an array of strings", 400)

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

        found_route = self.__route_service.generate_route(
            starting_point, restaurant_types, number_of_stops, length
        )
        features = [found_route["trajectory"]]
        for restaurant in found_route["restaurants"]:
            features.append(restaurant)

        return {"type": "FeatureCollection", "features": features}
