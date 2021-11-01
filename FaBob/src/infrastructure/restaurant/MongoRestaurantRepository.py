import json
from typing import List

from domain.Coordinates import Coordinates
from domain.restaurant.Restaurant import Restaurant
from pymongo import MongoClient

from domain.restaurant.RestaurantRepository import RestaurantRepository


class MongoRestaurantRepository(RestaurantRepository):
    def __init__(self, mongo_address: str, restaurant_data_filepath: str) -> None:
        self.mongo_client = MongoClient(mongo_address)
        self.restaurant_data_filepath = restaurant_data_filepath
        self.restaurants_database = self.mongo_client.epicurien
        self.restaurants_collection = self.restaurants_database["restaurants"]
        self.restaurants_collection.remove({})
        self.load_restaurants()

    def load_restaurants(self) -> None:
        restaurants = self.__read_restaurant_data_file()
        for restaurant in restaurants:
            self.restaurants_collection.insert(restaurant.to_dict())

    def __read_restaurant_data_file(self):
        restaurant_data_file = open(self.restaurant_data_filepath)
        restaurant_raw_data = json.load(restaurant_data_file)
        restaurants: List[Restaurant] = []
        for raw_restaurant in restaurant_raw_data:
            restaurants.append(self.__assemble_restaurant(raw_restaurant))
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
