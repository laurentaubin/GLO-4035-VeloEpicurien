import random
from typing import List

from pymongo import MongoClient

from domain.route.RouteRepository import RouteRepository


class MongoRouteRepository(RouteRepository):
    def __init__(self, mongo_address: str):
        self.__mongo_client = MongoClient(mongo_address)
        self.__database = self.__mongo_client.epicurien
        self.__routes_collection = self.__database["routes"]
        self.__routes_collection.create_index([("trajectory.properties.length", -1)])

    def find_starting_point(self, length: int, types: List[str]):
        route_documents = self.__find_routes_matching_length_and_types(length, types)
        random_route = random.choice(route_documents)
        return random_route["starting_point"]

    def find_route(
        self, starting_point: dict, types: List[str], length: int, number_of_stops: int
    ):
        route_documents = self.__find_routes_matching_length_and_types(length, types)
        random_route = random.choice(route_documents)

        desired_restaurants = self.__extract_desired_restaurants(
            types, random_route["restaurants"], number_of_stops
        )
        random_route["restaurants"] = desired_restaurants

        return random_route

    def __find_routes_matching_length_and_types(self, length, types):
        route_documents = []
        if len(types) == 0:
            cursor = self.__routes_collection.find(
                {
                    "trajectory.properties.length": {
                        "$gte": length * 0.9,
                        "$lte": length * 1.1,
                    }
                }
            )
        else:
            cursor = self.__routes_collection.find(
                {
                    "trajectory.properties.length": {
                        "$gte": length * 0.9,
                        "$lte": length * 1.1,
                    },
                    "types": {"$all": types},
                }
            )
        for document in cursor:
            route_documents.append(document)
        return route_documents

    def __extract_desired_restaurants(
        self, types: List[str], restaurants, number_of_stops
    ) -> List[dict]:
        desired_restaurants = []
        for restaurant in restaurants:
            if not set(restaurant["properties"]["type"]).isdisjoint(types):
                desired_restaurants.append(restaurant)

        if len(desired_restaurants) <= number_of_stops:
            return desired_restaurants
        return random.sample(desired_restaurants, number_of_stops)
