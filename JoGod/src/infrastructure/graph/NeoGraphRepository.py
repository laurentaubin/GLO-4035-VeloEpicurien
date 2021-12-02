import logging
import time

from py2neo import Graph

from domain.graph.GraphRepository import GraphRepository


class NeoGraphRepository(GraphRepository):
    def __init__(self, host: str, port: str):
        start = time.time()
        self.__graph_client = self.__get_graph_connection(host, port)
        print(f"\nTIME TO CONNECT TO NE04J : {time.time() - start}\n")

    def __get_graph_connection(self, host, port):
        while True:
            logging.warning("TRYING TO CONNECT TO NEO4J")
            time.sleep(1)
            try:
                return Graph(host=host, port=port)
            except Exception as e:
                logging.warning("ERROR CONNECTING TO NEO: {0}, TRYING AGAIN".format(e))
                pass

    def get_starting_vertex_node(self, starting_point: dict):
        latitude = starting_point["coordinates"][1]
        longitude = starting_point["coordinates"][0]

        return {}
