import random
from typing import List

from pymongo import MongoClient

from domain.route.RouteRepository import RouteRepository


class MongoRouteRepository(RouteRepository):
    def __init__(self, mongo_address: str):
        self.__mongo_client = MongoClient(mongo_address)
        self.__database = self.__mongo_client.epicurien
        self.__routes_collection = self.__database["routes"]

    def find_starting_point(self, length: int, types: List[str]):
        route_documents = []
        if len(types) == 0:
            cursor = self.__routes_collection.find(
                {"trajectory.properties.length": {"$gte": length * 0.9, "$lte": length * 1.1}})
        else:
            cursor = self.__routes_collection.find(
                {"trajectory": {"properties": {"length": {"$gte": length * 0.9, "$lte": length * 1.1}}},
                 "restaurants": {"properties": {"types": {"$all": types}}}})
        for document in cursor:
            route_documents.append(document)


        random_route = random.choice(route_documents)
        print("SELECTED ROUTE: ")
        print("LENGTH: ", random_route["trajectory"]["properties"]["length"])
        restaurant_types_encounter_on_route = self.__extract_restaurant_types(random_route["restaurants"])
        print("TYPES: ", restaurant_types_encounter_on_route)
        return random_route["starting_point"]

    def __extract_restaurant_types(self, restaurant_documents):
        all_types = set()
        for restaurant_document in restaurant_documents:
            types = restaurant_document["properties"]["type"]
            for type in types:
                all_types.add(type)
        return list(all_types)
