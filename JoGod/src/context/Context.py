from config import Config
from api.HeartbeatResource import HeartbeatResource
from server.ApplicationServer import ApplicationServer


class Context:
    def __init__(self):
        self.__application_server = self.__create_application_server()

    def run(self):
        self.__application_server.run()

    def __create_application_server(self):
        heartbeat_resource = HeartbeatResource(Config.CHOSEN_CITY)
        return ApplicationServer(heartbeat_resource)
