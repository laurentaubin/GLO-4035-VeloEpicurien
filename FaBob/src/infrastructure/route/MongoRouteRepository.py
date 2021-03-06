from pymongo import MongoClient

from domain.route.RouteRepository import RouteRepository


class MongoRouteRepository(RouteRepository):
    def __init__(self, mongo_address: str):
        self.__mongo_client = MongoClient(mongo_address)
        self.__database = self.__mongo_client.epicurien
        self.__routes_collection = self.__database["routes"]
        self.__routes_collection.create_index(
            [("geometry", "2dsphere")], name="starting_point"
        )

    def save_routes(self, routes: dict):
        for route in routes:
            trajectory_feature = self.__assemble_trajectory_feature(
                route["route_coordinates"], route["length"]
            )
            restaurant_documents = self.__assemble_restaurant_features(
                route["restaurants"]
            )
            starting_point = self.__assemble_starting_point(route["starting_point"])
            self.__routes_collection.insert(
                {
                    "trajectory": trajectory_feature,
                    "restaurants": restaurant_documents,
                    "starting_point": starting_point,
                }
            )

    def add_types(self):
        cursor = self.__routes_collection.find()
        for doc in cursor:
            restaurant_types_in_route = set()
            restaurants = doc["restaurants"]
            for restaurant in restaurants:
                for restaurant_type in restaurant["properties"]["type"]:
                    restaurant_types_in_route.add(restaurant_type)
            doc_id = doc["_id"]
            self.__routes_collection.update(
                {"_id": doc_id}, {"$set": {"types": list(restaurant_types_in_route)}}
            )

    def __assemble_trajectory_feature(self, route_coordinates, length):
        return {
            "type": "Feature",
            "geometry": {"type": "MultiLineString", "coordinates": [route_coordinates]},
            "properties": {"length": length},
        }

    def __assemble_restaurant_features(self, restaurants):
        restaurant_documents = []
        for restaurant in restaurants:
            restaurant_documents.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": restaurant["coordinates"],
                    },
                    "properties": {
                        "name": restaurant["name"],
                        "type": restaurant["types"],
                    },
                }
            )

        return restaurant_documents

    def __assemble_starting_point(self, starting_point_coordinates):
        return {
            "geometry": {"type": "Point", "coordinates": starting_point_coordinates}
        }
