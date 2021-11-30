from flask import Flask

from api.LoaderResource import LoaderResource


class ApplicationServer:
    def __init__(self, loader_resource: LoaderResource):
        self.__app = Flask(__name__)
        self.__loader_resource = loader_resource

        self.__app.config["JSON_AS_ASCII"] = False

        self.__app.add_url_rule(
            "/load_segments", "load_segments", self.__load_segments, methods=["POST"]
        )

    def run(self, hostname) -> None:
        self.__app.run(hostname)

    def __load_segments(self):
        return self.__loader_resource.load_segments()
