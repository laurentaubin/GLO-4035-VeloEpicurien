import logging
import time
from math import pi, cos, asin, sqrt
from time import sleep
from typing import List, Dict

from py2neo import Graph, Node, Relationship

from domain.Coordinate import Coordinate
from domain.restaurant.Restaurant import Restaurant
from domain.segment.Vertex import Vertex


class NeoGraphRepository:
    __MIN_DISTANCE_OUTSIDE_OFFICIAL_PATH = 25
    __WIPE_COMMAND = "MATCH (n) DETACH DELETE n"
    __GET_ALL_VERTEXES = "MATCH (vertex:Vertex) RETURN vertex"

    def __init__(self, host: str, port: str):
        self.__connected_segments: Dict[str, List[str]] = {}
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
        number_of_fetch_saved = 0
        relationships = []

        # Collect source segment vertexes
        source_vertexes_nodes: List[Node] = []
        source_vertexes_result = self.__fetch_segment_vertexes_by_id(source_segment_id)
        source_vertexes_entries = source_vertexes_result.to_table()
        for source_vertex_node_entry in source_vertexes_entries:
            source_vertexes_nodes.append(source_vertex_node_entry[0])

        # Collect only near vertexes of segments not already connected
        near_vertexes_nodes: List[Node] = []
        for near_segment_id in near_segments:
            if near_segment_id in self.__connected_segments:
                if source_segment_id in self.__connected_segments.get(near_segment_id):
                    number_of_fetch_saved += 1
                    pass
            near_segment_vertexes_result = self.__fetch_segment_vertexes_by_id(near_segment_id)
            near_vertexes_entries = near_segment_vertexes_result.to_table()
            for near_vertex_node_entry in near_vertexes_entries:
                near_vertexes_nodes.append(near_vertex_node_entry[0])

        # Connect source vertexes node to near vertexes nodes
        for source_vertex_node in source_vertexes_nodes:
            source_vertex = self.__assemble_vertex(source_vertex_node)
            for near_vertex_node in near_vertexes_nodes:
                near_vertex = self.__assemble_vertex(near_vertex_node)
                distance = self.__calculate_distance_between_vertex(source_vertex, near_vertex)
                if distance <= self.__MIN_DISTANCE_OUTSIDE_OFFICIAL_PATH:
                    # Bidirectional relationship, enable caching of already connected segments
                    relationships.append(
                        Relationship(source_vertex_node, "link_to", near_vertex_node, distance=distance))
                    relationships.append(
                        Relationship(near_vertex_node, "link_to", source_vertex_node, distance=distance))

        self.__connected_segments[source_segment_id] = near_segments

        for relationship in relationships:
            self.__graph_client.create(relationship)
        print("NUMBER OF FETCH SAVED: {0}".format(str(number_of_fetch_saved)))
        return number_of_fetch_saved

    def save_restaurant(self, restaurant: Restaurant):
        restaurant_node = Node("Restaurant", latitude=str(restaurant.get_coordinates().get_latitude()),
                               longitude=str(restaurant.get_coordinates().get_longitude()),
                               restaurant_id=restaurant.get_id(), types=restaurant.get_types())
        self.__graph_client.create(restaurant_node)

        vertex_nodes: List[Node] = []
        for segment_id in restaurant.get_near_segments():
            near_segment_vertexes_result = self.__fetch_segment_vertexes_by_id(segment_id)
            near_vertexes_entries = near_segment_vertexes_result.to_table()
            for near_vertex_node_entry in near_vertexes_entries:
                vertex_nodes.append(near_vertex_node_entry[0])

        vertex_closest_to_restaurant = None
        min_distance_with_restaurant = float("inf")
        for vertex_node in vertex_nodes:
            vertex = self.__assemble_vertex(vertex_node)
            distance = self.__calculate_distance(vertex.get_coordinate(), restaurant.get_coordinates())
            if distance < min_distance_with_restaurant:
                min_distance_with_restaurant = distance
                vertex_closest_to_restaurant = vertex_node
        if vertex_closest_to_restaurant is None:
            return "NOT CONNECTED"
        self.__graph_client.create(Relationship(restaurant_node, "on_path", vertex_closest_to_restaurant))
        return min_distance_with_restaurant

    def __calculate_distance(self, first_coordinates: Coordinate, second_coordinates: Coordinate):
        p = pi / 180
        a = 0.5 - cos((second_coordinates.get_latitude() - first_coordinates.get_latitude()) * p) / 2 + cos(
            first_coordinates.get_latitude() * p) * cos(second_coordinates.get_latitude() * p) * (1 - cos(
            (second_coordinates.get_longitude() - first_coordinates.get_longitude()) * p)) / 2
        return 12742000 * asin(sqrt(a))

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

    def __fetch_segment_vertexes_by_id(self, segment_id: str):
        return self.__graph_client.run(
            "MATCH (vertex: Vertex {segment_id: '" + str(segment_id) + "'}) RETURN vertex")
