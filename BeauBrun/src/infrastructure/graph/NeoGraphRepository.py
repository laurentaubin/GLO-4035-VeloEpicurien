from typing import List

from py2neo import Graph


class NeoGraphRepository:
    def __init__(self, connection_string: str):
        self.__graph_client = Graph(connection_string)

    def load_segments(self, segments: List[dict]) -> None:



        pass
