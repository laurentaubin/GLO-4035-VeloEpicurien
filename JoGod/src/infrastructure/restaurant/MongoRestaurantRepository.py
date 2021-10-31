from pymongo import MongoClient

from domain.restaurant.RestaurantRepository import RestaurantRepository


class MongoRestaurantRepository(RestaurantRepository):
    def __init__(self, mongo_address: str):
        self.mongo_client = MongoClient(mongo_address)
        self.restaurants_database = self.mongo_client.epicurien
        self.restaurants_collection = self.restaurants_database["restaurants"]

    def get_total_number_of_restaurants(self) -> int:
        return self.restaurants_collection.find().count()
