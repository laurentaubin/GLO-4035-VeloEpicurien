from flask import Flask


class ApplicationServer:
    def __init__(self):
        self.__app = Flask(__name__)
        self.__app.config["JSON_AS_ASCII"] = False

    def run(self, hostname) -> None:
        self.__app.run(hostname)
