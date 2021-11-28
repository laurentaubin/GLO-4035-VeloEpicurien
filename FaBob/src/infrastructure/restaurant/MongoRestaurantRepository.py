import json
from typing import List

from domain.Coordinates import Coordinates
from domain.restaurant.Restaurant import Restaurant
from pymongo import MongoClient

from domain.restaurant.RestaurantRepository import RestaurantRepository


class MongoRestaurantRepository(RestaurantRepository):
    def __init__(self, mongo_address: str, restaurant_data_filepath: str) -> None:
        self.__mongo_client = MongoClient(mongo_address)
        self.__restaurant_data_filepath = restaurant_data_filepath
        self.__restaurants_database = self.__mongo_client.epicurien
        self.__restaurants_collection = self.__restaurants_database["restaurants"]
        self.__restaurants_collection.remove({})

    def load_restaurants(self) -> None:
        restaurants = self.__read_restaurant_data_file()
        for restaurant in restaurants:
            self.__restaurants_collection.insert(restaurant.to_dict())

    def find_all(self) -> List[Restaurant]:
        restaurant_documents = self.__restaurants_collection.find()
        restaurants = []
        for restaurant_document in restaurant_documents:
            restaurants.append(self.__assemble_restaurant_from_document(restaurant_document))
        return restaurants

    def update(self, restaurant: Restaurant):
        self.__restaurants_collection.update_one({"id": restaurant.get_id()},
                                                 {"$set": {"near_segments": restaurant.get_near_segments()}},
                                                 upsert=False)

    def __read_restaurant_data_file(self):
        with open(self.__restaurant_data_filepath) as restaurant_data_file:
            restaurant_raw_data = json.load(restaurant_data_file)
            restaurants: List[Restaurant] = []
            for raw_restaurant in restaurant_raw_data:
                restaurant = self.__assemble_restaurant(raw_restaurant)
                restaurant.set_geometry({"type": "Point", "coordinates": [restaurant.get_coordinates().get_longitude(),
                                                                          restaurant.get_coordinates().get_latitude()]})
                restaurants.append(restaurant)
            return restaurants

    def __assemble_restaurant(self, restaurant_data_entry) -> Restaurant:
        identifier: str = restaurant_data_entry["id"]
        name: str = restaurant_data_entry["name"]
        coordinates: Coordinates = Coordinates(
            restaurant_data_entry["coordinates"]["latitude"],
            restaurant_data_entry["coordinates"]["longitude"],
        )
        types = restaurant_data_entry["categories"]
        return Restaurant(identifier, name, coordinates, types)

    def __assemble_restaurant_from_document(self, restaurant_document) -> Restaurant:
        identifier: str = restaurant_document["id"]
        name: str = restaurant_document["name"]
        coordinates: Coordinates = Coordinates(
            restaurant_document["coordinates"]["latitude"],
            restaurant_document["coordinates"]["longitude"],
        )
        types = restaurant_document["types"]
        geometry = restaurant_document["geometry"]
        restaurant = Restaurant(identifier, name, coordinates, types)
        restaurant.set_geometry(geometry)
        return restaurant
