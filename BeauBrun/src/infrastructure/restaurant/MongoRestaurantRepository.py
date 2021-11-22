from typing import List

from domain.Coordinate import Coordinate
from domain.restaurant.Restaurant import Restaurant
from pymongo import MongoClient

from domain.restaurant.RestaurantRepository import RestaurantRepository


class MongoRestaurantRepository(RestaurantRepository):
    def __init__(self, mongo_address: str) -> None:
        self.__mongo_client = MongoClient(mongo_address)
        self.__restaurants_database = self.__mongo_client.epicurien
        self.__restaurants_collection = self.__restaurants_database["restaurants"]

    def find_all(self) -> List[Restaurant]:
        restaurant_documents = self.__restaurants_collection.find({})
        restaurants: List[Restaurant] = []
        for restaurant_document in restaurant_documents:
            restaurants.append(self.__assemble_restaurant(restaurant_document))
        return restaurants

    def __assemble_restaurant(self, restaurant_document) -> Restaurant:
        identifier: str = restaurant_document["id"]
        name: str = restaurant_document["name"]
        coordinates: Coordinate = Coordinate(
            restaurant_document["coordinates"]["latitude"],
            restaurant_document["coordinates"]["longitude"],
        )
        types = restaurant_document["categories"]
        return Restaurant(identifier, name, coordinates, types)
