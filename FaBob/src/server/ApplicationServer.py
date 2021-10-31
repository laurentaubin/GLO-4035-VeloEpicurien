from flask import Flask

from api.LoaderResource import LoaderResource


class ApplicationServer:
    def __init__(self, loader_resource):
        self.__loader_resource = loader_resource

        self.__app = Flask(__name__)
        self.__app.config["JSON_AS_ASCII"] = False
        self.__app.add_url_rule("/load", "load", self.__load_data())

    def run(self, hostname) -> None:
        self.__app.run(hostname)

    def __load_data(self) -> None:
        pass
        # return self.__loader_resource.load_restaurants()
