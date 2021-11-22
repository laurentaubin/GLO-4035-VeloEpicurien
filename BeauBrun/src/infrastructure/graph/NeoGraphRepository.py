from typing import List

from py2neo import Graph, Node, Relationship

from domain.segment.Vertex import Vertex


class NeoGraphRepository:
    NODE_QUERY = "MATCH (vertex:Vertex {segment_id: '{segment_id}', latitude: {latitude}, longitude: {longitude}) RETURN vertex"

    def __init__(self, connection_string: str):
        self.__graph_client = Graph(connection_string)

    def save_vertexes(self, vertexes: List[Vertex]) -> None:
        for vertex in vertexes:
            vertex_coordinate = vertex.get_coordinate()
            vertex_node = Node("Vertex", latitude=vertex_coordinate.get_latitude(),
                               longitude=vertex_coordinate.get_longitude(), segment_id=vertex.get_id())
            self.__graph_client.create(vertex_node)

    def save_vertexes_relationship(self, first_vertex: Vertex, second_vertex: Vertex, distance: float):
        first_vertex_node = self.__match_vertex(first_vertex)
        second_vertex = self.__match_vertex(second_vertex)
        vertex_relationship = Relationship(first_vertex_node, "link_to", second_vertex, distance=distance)
        self.__graph_client.create(vertex_relationship)

    def load_segments(self, segments: List[dict]) -> None:
        pass

    def __match_vertex(self, vertex: Vertex) -> Node:
        return self.__graph_client.run(
            self.NODE_QUERY.format(segment_id=vertex.get_id(), latitude=vertex.get_coordinate().get_latitude(),
                                   longitude=vertex.get_coordinate().get_longitude()))
