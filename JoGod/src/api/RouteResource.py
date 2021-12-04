from typing import List

from flask import request, make_response
from service.RouteService import RouteService
from domain.restaurant.RestaurantRepository import RestaurantRepository

from jsonschema import validate


class RouteResource:
    def __init__(self, route_service: RouteService, restaurant_repository: RestaurantRepository):
        self.__route_service = route_service
        self.__restaurant_repository = restaurant_repository

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
            "properties": {"type": {"type": "array"}},
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
        format_validation = self.__validate_request_format(body)
        print("format")
        print(format_validation.status)
        if format_validation.status != "200 OK":
            return format_validation

        field_validation = self.__validate_request_fields(body)
        print("field")
        print(field_validation.status)
        if field_validation.status != "200 OK":
            return field_validation

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

    def __validate_request_format(self, body):
        error_message = ""
        if not body:
            error_message += "empty body\n"

        if "length" not in body:
            error_message += "body must contain field 'length'\n"

        if "type" not in body:
            error_message += "body must contain field 'type'\n"

        if "startingPoint" not in body:
            error_message += "body must contain field 'startingPoint'\n"

        if "numberOfStops" not in body:
            error_message += "body must contain field 'numberOfStops'\n"

        if not isinstance(body["length"], int):
            error_message += "''length' must be an integer\n"

        for desired_type in body["type"]:
            if not isinstance(desired_type, str):
                error_message += "'type' must be an array of strings\n"

        if not isinstance(body["numberOfStops"], int):
            error_message += "''numberOfStops' must be an integer\n"

        if not isinstance(body["startingPoint"], dict):
            error_message += "''startingPoint' must be a geojson object\n"

        schema = {
            "type": "object",
            "properties": {"type": {"type": "array"}},
        }

        try:
            validate(body, schema)
        except Exception:
            error_message += "'type' must be an array of strings\n"

        if error_message == "":
            return make_response("", 200)

        return make_response(error_message, 400)

    def __validate_request_fields(self, body):
        error_message = ""
        if body["length"] <= 0:
            error_message += "invalid value for 'length'"

        valid_types = self.__restaurant_repository.get_restaurant_types()
        for type in body["type"]:
            if type not in valid_types:
                error_message += "'type' contains invalid types"
                break

        if error_message == "":
            return make_response("", 200)

        return make_response(error_message, 404)


