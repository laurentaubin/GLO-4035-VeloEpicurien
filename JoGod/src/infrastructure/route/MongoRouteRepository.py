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
        route_documents = []
        if len(types) == 0:
            cursor = self.__routes_collection.find(
                {"trajectory.properties.length": {"$gte": length * 0.9, "$lte": length * 1.1}})
        else:
            cursor = self.__routes_collection.find(
                {"trajectory.properties.length": {"$gte": length * 0.9, "$lte": length * 1.1},
                 "types": {"$all": types}})
        for document in cursor:
            route_documents.append(document)

        random_route = random.choice(route_documents)
        return random_route["starting_point"]

    def find_starting_point_with_types(self):
        cursor = self.__routes_collection.find()
        for doc in cursor:
            restaurant_types_in_route = set()
            restaurants = doc["restaurants"]
            for restaurant in restaurants:
                for restaurant_type in restaurant["properties"]["type"]:
                    restaurant_types_in_route.add(restaurant_type)
            doc_id = doc["_id"]
            self.__routes_collection.update({"_id": doc_id}, {"$set": {"types": list(restaurant_types_in_route)}})
