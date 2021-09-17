from flask import Flask

from api.HeartbeatResource import HeartbeatResource


class ApplicationServer:
    def __init__(self, heartbeat_resource: HeartbeatResource):
        self.__heartbeat_resource = heartbeat_resource

        self.__app = Flask(__name__)
        self.__app.config['JSON_AS_ASCII'] = False
        self.__app.add_url_rule("/heartbeat", "heartbeat", self.__send_heartbeat)

    def run(self):
        self.__app.run("0.0.0.0")

    def __send_heartbeat(self):
        return self.__heartbeat_resource.send_heartbeat().to_dict()
