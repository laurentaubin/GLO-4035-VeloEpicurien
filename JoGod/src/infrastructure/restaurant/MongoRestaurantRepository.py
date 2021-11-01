from pymongo import MongoClient

from domain.restaurant.RestaurantRepository import RestaurantRepository


class MongoRestaurantRepository(RestaurantRepository):
    def __init__(self, mongo_address: str):
        self.mongo_client = MongoClient(mongo_address)
        self.restaurants_database = self.mongo_client.epicurien
        self.restaurants_collection = self.restaurants_database["restaurants"]

    def get_total_number_of_restaurants(self) -> int:
        return self.restaurants_collection.find().count()

    def get_number_of_restaurants_per_type(self) -> dict:
        number_of_restaurants_per_type = {}
        cursor = self.restaurants_collection.aggregate([
            {
                "$unwind": "$types"
            },
            {
                "$group":
                    {
                        "_id": "$types.title",
                        "count": {"$sum": 1}
                    }
            }
        ])
        for entry in cursor:
            number_of_restaurants_per_type[entry.get("_id")] = entry.get("count")
        return number_of_restaurants_per_type
