from flask import Flask

from api.HeartbeatResource import HeartbeatResource
from api.RestaurantResource import RestaurantResource


class ApplicationServer:
    def __init__(self, heartbeat_resource: HeartbeatResource, restaurant_resource: RestaurantResource):
        self.__heartbeat_resource = heartbeat_resource
        self.__restaurant_resource = restaurant_resource

        self.__app = Flask(__name__)
        self.__app.config["JSON_AS_ASCII"] = False
        self.__app.add_url_rule("/heartbeat", "heartbeat", self.__send_heartbeat)

        self.__app.add_url_rule("/extracted_data", "extracted_data", self.__get_extracted_data)

    def run(self, hostname) -> None:
        self.__app.run(hostname)

    def __send_heartbeat(self) -> dict:
        return self.__heartbeat_resource.send_heartbeat().to_dict()

    def __get_extracted_data(self) -> dict:
        return {"nbRestaurants": self.__restaurant_resource.get_total_number_of_restaurants()}
