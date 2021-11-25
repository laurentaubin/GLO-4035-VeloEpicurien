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

        start = time.time()
        self.__graph_client.run(self.__WIPE_COMMAND)
        print(f'\nTIME TO WIPE DATABASE : {time.time() - start}\n')
        vertexes = self.__graph_client.run(self.__GET_ALL_VERTEXES)
        vertex_list = list(vertexes)
        if (len(vertex_list) == 0):
            print("\n DATABASE WAS REALLY WIPED\n")
        else:
            print("\n DATABASE WAS NOT REALLY WIPED\n")

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
                               longitude=str(vertex_coordinate.get_longitude()), segment_id=vertex.get_id())
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
        return self.__number_of_nodes

    def connect_near_vertexes(self):
        cursor = self.__graph_client.run(self.__GET_ALL_VERTEXES)
        vertex_nodes = list(cursor)
        for vertex_node in vertex_nodes:
            vertex = self.__assemble_vertex(vertex_node)
            for another_vertex_node in vertex_nodes:
                if another_vertex_node["segment_id"] == vertex_node["segment_id"]:
                    pass
                another_vertex = self.__assemble_vertex(another_vertex_node)
                distance = self.__calculate_distance_between_vertex(vertex, another_vertex)
                if distance <= self.__MIN_DISTANCE_OUTSIDE_OFFICIAL_PATH:
                    print("Distance between vertex: " + str(distance))
                    self.__save_vertexes_relationship(vertex_node, another_vertex_node, distance)

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
