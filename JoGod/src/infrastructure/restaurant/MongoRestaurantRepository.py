from pymongo import MongoClient

from domain.restaurant.RestaurantRepository import RestaurantRepository


class MongoRestaurantRepository(RestaurantRepository):
    def __init__(self, mongo_address: str):
        self.__mongo_client = MongoClient(mongo_address)
        self.__restaurants_database = self.__mongo_client.epicurien
        self.__restaurants_collection = self.__restaurants_database["restaurants"]

    def get_total_number_of_restaurants(self) -> int:
        return self.__restaurants_collection.find().count()

    def get_number_of_restaurants_per_type(self) -> dict:
        number_of_restaurants_per_type = {}
        cursor = self.__restaurants_collection.aggregate(
            [
                {"$unwind": "$types"},
                {"$group": {"_id": "$types.title", "count": {"$sum": 1}}},
            ]
        )
        for entry in cursor:
            number_of_restaurants_per_type[entry.get("_id")] = entry.get("count")
        return number_of_restaurants_per_type

    def get_restaurant_types(self) -> list:
        restaurant_types = []
        cursor = self.__restaurants_collection.aggregate(
            [
                {"$unwind": "$types"},
                {"$group": {"_id": "$types.alias"}},
            ]
        )
        for entry in cursor:
            restaurant_types.append(entry.get("_id"))

        return restaurant_types

