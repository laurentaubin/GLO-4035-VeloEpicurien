from math import pi, cos, asin, sqrt
from time import sleep
from typing import List

from py2neo import Graph, Node, Relationship

from domain.segment.Vertex import Vertex


class NeoGraphRepository:
    def __init__(self, host: str, port: str):
        self.__graph_client = self.__get_graph_connection(host, port)

    def __get_graph_connection(self, host, port):
        while True:
            print("[SLEEP] sleep starts")
            sleep(10)
            print("[SLEEP] sleep ended")
            try:
                print("[NEO] ATTEMPTING CONNECTION")
                return Graph(host=host, port=port)
            except:
                print("[NEO] FAILED TO CONNECT")
                pass

    def save_vertexes(self, vertexes: List[Vertex]) -> None:
        vertex_nodes = []
        for vertex in vertexes:
            vertex_coordinate = vertex.get_coordinate()
            vertex_node = Node("Vertex", latitude=str(vertex_coordinate.get_latitude()),
                               longitude=str(vertex_coordinate.get_longitude()), segment_id=vertex.get_id())
            self.__graph_client.create(vertex_node)
            vertex_nodes.append(vertex_node)
        for index, _ in enumerate(vertex_nodes):
            if index != len(vertex_nodes) - 1:
                first_vertex_node = vertex_nodes[index]
                second_vertex_node = vertex_nodes[index + 1]
                distance = self.__calculate_distance_between_vertex(vertexes[index], vertexes[index + 1])
                self.save_vertexes_relationship(first_vertex_node, second_vertex_node, distance)

    def save_vertexes_relationship(self, first_vertex_node: Node, second_vertex_node: Node, distance: float):
        vertex_relationship = Relationship(first_vertex_node, "link_to", second_vertex_node, distance=distance)
        self.__graph_client.create(vertex_relationship)

    def load_segments(self, segments: List[dict]) -> None:
        pass

    def __calculate_distance_between_vertex(self, first_vertex: Vertex, second_vertex: Vertex):
        first_vertex_coordinate = first_vertex.get_coordinate()
        second_vertex_coordinate = second_vertex.get_coordinate()
        p = pi / 180
        a = 0.5 - cos((second_vertex_coordinate.get_latitude() - first_vertex_coordinate.get_latitude()) * p) / 2 + cos(
            first_vertex_coordinate.get_latitude() * p) * cos(second_vertex_coordinate.get_latitude() * p) * (1 - cos(
            (second_vertex_coordinate.get_longitude() - first_vertex_coordinate.get_longitude()) * p)) / 2
        return 12742000 * asin(sqrt(a))
