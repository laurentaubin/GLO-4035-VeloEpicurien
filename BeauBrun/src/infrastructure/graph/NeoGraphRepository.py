import logging
import time
from math import pi, cos, asin, sqrt
from time import sleep
from typing import List

from py2neo import Graph, Node, Relationship

from domain.Coordinate import Coordinate
from domain.segment.Vertex import Vertex


class NeoGraphRepository:
    __MIN_DISTANCE_OUTSIDE_OFFICIAL_PATH = 50
    __WIPE_COMMAND = "MATCH (n) DETACH DELETE n"
    __GET_ALL_VERTEXES = "MATCH (vertex:Vertex) RETURN vertex"

    def __init__(self, host: str, port: str):
        self.__number_of_nodes = 0
        start = time.time()
        self.__graph_client = self.__get_graph_connection(host, port)
        print(f'\nTIME TO CONNECT TO NE04J : {time.time() - start}\n')

    def __get_graph_connection(self, host, port):
        while True:
            logging.warning("TRYING TO CONNECT TO NEO4J")
            sleep(1)
            try:
                return Graph(host=host, port=port)
            except Exception as e:
                logging.warning("ERROR CONNECTING TO NEO: {0}, TRYING AGAIN".format(e))
                pass

    def save_vertexes(self, vertexes: List[Vertex]) -> None:
        vertex_nodes = []
        for vertex in vertexes:
            vertex_coordinate = vertex.get_coordinate()
            vertex_node = Node("Vertex", latitude=str(vertex_coordinate.get_latitude()),
                               longitude=str(vertex_coordinate.get_longitude()), segment_id=str(vertex.get_id()))
            self.__graph_client.create(vertex_node)
            vertex_nodes.append(vertex_node)
            self.__number_of_nodes += 1
        for index, _ in enumerate(vertex_nodes):
            if index != len(vertex_nodes) - 1:
                first_vertex_node = vertex_nodes[index]
                second_vertex_node = vertex_nodes[index + 1]
                distance = self.__calculate_distance_between_vertex(vertexes[index], vertexes[index + 1])
                self.__save_vertexes_relationship(first_vertex_node, second_vertex_node, distance)

    def __save_vertexes_relationship(self, first_vertex_node: Node, second_vertex_node: Node, distance: float):
        vertex_relationship = Relationship(first_vertex_node, "link_to", second_vertex_node, distance=distance)
        self.__graph_client.create(vertex_relationship)

    def get_number_of_vertexes(self):
        return len(list(self.__graph_client.run(self.__GET_ALL_VERTEXES)))

    def connect_vertexes(self, source_segment_id: str, near_segments: List[str]):
        relationships = []
        source_vertexes_cursor = self.__graph_client.run(
            "MATCH (vertex: Vertex {segment_id: '" + str(source_segment_id) + "'}) RETURN vertex")
        source_vertexes_nodes = source_vertexes_cursor.to_table()
        for source_vertex_node_cursor in source_vertexes_nodes:
            source_vertex_node = source_vertex_node_cursor[0]
            source_vertex = self.__assemble_vertex(source_vertex_node)
            for near_segment_id in near_segments:
                if near_segment_id in self.__connected_segments:
                    if source_segment_id in self.__connected_segments.get(near_segment_id):
                        pass
                near_segment_vertexes_cursor = self.__graph_client.run(
                    "MATCH (vertex: Vertex {segment_id: '" + str(near_segment_id) + "'}) RETURN vertex")
                near_vertexes_nodes = near_segment_vertexes_cursor.to_table()
                for near_vertex_node_cursor in near_vertexes_nodes:
                    near_vertex_node = near_vertex_node_cursor[0]
                    near_vertex = self.__assemble_vertex(near_vertex_node)
                    distance = self.__calculate_distance_between_vertex(source_vertex, near_vertex)
                    if distance <= self.__MIN_DISTANCE_OUTSIDE_OFFICIAL_PATH:
                        print(distance)
                        relationships.append(
                            Relationship(source_vertex_node, "link_to", near_vertex_node, distance=distance))
                        relationships.append(
                            Relationship(near_vertex_node, "link_to", source_vertex_node, distance=distance))
        for relationship in relationships:
            self.__graph_client.create(relationship)

    def connect_near_vertexes(self):
        relationships = []
        cursor = self.__graph_client.run(self.__GET_ALL_VERTEXES)
        vertex_nodes = cursor.to_table()
        for vertex_node_cursor in vertex_nodes:
            vertex_node = vertex_node_cursor[0]
            vertex = self.__assemble_vertex(vertex_node)
            for another_vertex_node_cursor in vertex_nodes:
                another_vertex_node = another_vertex_node_cursor[0]
                if another_vertex_node["segment_id"] == vertex_node["segment_id"]:
                    pass
                another_vertex = self.__assemble_vertex(another_vertex_node)
                distance = self.__calculate_distance_between_vertex(vertex, another_vertex)
                if distance <= self.__MIN_DISTANCE_OUTSIDE_OFFICIAL_PATH:
                    relationships.append(Relationship(vertex_node, "link_to", another_vertex_node, distance=distance))

    def __calculate_distance_between_vertex(self, first_vertex: Vertex, second_vertex: Vertex):
        first_vertex_coordinate = first_vertex.get_coordinate()
        second_vertex_coordinate = second_vertex.get_coordinate()
        p = pi / 180
        a = 0.5 - cos((second_vertex_coordinate.get_latitude() - first_vertex_coordinate.get_latitude()) * p) / 2 + cos(
            first_vertex_coordinate.get_latitude() * p) * cos(second_vertex_coordinate.get_latitude() * p) * (1 - cos(
            (second_vertex_coordinate.get_longitude() - first_vertex_coordinate.get_longitude()) * p)) / 2
        return 12742000 * asin(sqrt(a))

    def __assemble_vertex(self, vertex_node: Node):
        return Vertex(vertex_node["segment_id"],
                      Coordinate(float(vertex_node["latitude"]), float(vertex_node["longitude"])))
