from math import pi, cos, asin, sqrt
from typing import List

from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.Segment import Segment
from domain.segment.SegmentRepository import SegmentRepository
from domain.segment.Vertex import Vertex
from infrastructure.graph.NeoGraphRepository import NeoGraphRepository


class GraphService:
    def __init__(self, graph_repository: NeoGraphRepository, segment_repository: SegmentRepository,
                 restaurant_repository: RestaurantRepository):
        self.__graph_repository = graph_repository
        self.__segment_repository = segment_repository
        self.__restaurant_repository = restaurant_repository

    def load_segments(self) -> None:
        segments: List[Segment] = self.__segment_repository.find_all()
        for segment in segments:
            vertexes = self.__create_segment_vertexes(segment)
            self.__graph_repository.save_vertexes(vertexes)
            self.__save_vertexes_relationships(vertexes)

    def connect_near_segments_together(self) -> None:
        pass

    def connect_restaurants_to_segments(self) -> None:
        pass

    def __save_vertexes_relationships(self, vertexes: List[Vertex]) -> None:
        for index, _ in enumerate(vertexes):
            if index != len(vertexes) - 1:
                first_vertex = vertexes[index]
                second_vertex = vertexes[index + 1]
                distance = self.__calculate_distance_between_vertex(first_vertex, second_vertex)
                self.__graph_repository.save_vertexes_relationship(first_vertex, second_vertex, distance)

    def __create_segment_vertexes(self, segment: Segment):
        vertexes = []
        for coordinate in segment.get_geometry().get_coordinates():
            vertexes.append(Vertex(segment.get_id(), coordinate))
        return vertexes

    def __calculate_distance_between_vertex(self, first_vertex: Vertex, second_vertex: Vertex):
        first_vertex_coordinate = first_vertex.get_coordinate()
        second_vertex_coordinate = second_vertex.get_coordinate()
        p = pi / 180
        a = 0.5 - cos((second_vertex_coordinate.get_latitude() - first_vertex_coordinate.get_latitude()) * p) / 2 + cos(
            first_vertex_coordinate.get_latitude() * p) * cos(second_vertex_coordinate.get_latitude() * p) * (1 - cos(
            (second_vertex_coordinate.get_longitude() - first_vertex_coordinate.get_longitude()) * p)) / 2
        return 12742 * asin(sqrt(a))
