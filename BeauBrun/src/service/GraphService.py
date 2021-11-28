import time
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
        print("\nSTARTING TO LOAD SEGMENTS IN GRAPH\n")
        start = time.time()
        segments: List[Segment] = self.__segment_repository.find_all()
        for segment in segments:
            vertexes = self.__create_segment_vertexes(segment)
            self.__graph_repository.save_vertexes(vertexes)
        print(f'\nTIME TO LOAD SEGMENTS IN GRAPH: {time.time() - start}\n')

    def connect_near_segments_together(self) -> None:
        number_of_fetch_saved = 0
        print("\n CONNECTING NEAR VERTEXES\n")
        start = time.time()
        segments: List[Segment] = self.__segment_repository.find_all()
        for segment in segments:
            number_of_fetch_saved += self.__graph_repository.connect_vertexes(segment.get_segment_id(),
                                                                              segment.get_near_segments())
            print("\nTOTAL NUMBER OF FETCH SAVED: {0}".format(str(number_of_fetch_saved)))

        print(f'\nTIME TO CONNECT NEAR VERTEXES : {time.time() - start}\n')

    def connect_restaurants_to_segments(self) -> None:
        print("\n CONNECTING RESTAURANTS TO VERTEXES")
        start = time.time()
        restaurants = self.__restaurant_repository.find_all()
        number_of_restaurants_connected = 0
        total_number_of_restaurants = len(restaurants)
        for restaurant in restaurants:
            self.__graph_repository.save_restaurant(restaurant)
            number_of_restaurants_connected += 1
            print("\n RESTAURANT {name} CONNECTED - {nbr_connected}/{total}".format(name=restaurant.get_name(),
                                                                                    nbr_connected=str(
                                                                                        number_of_restaurants_connected),
                                                                                    total=str(
                                                                                        total_number_of_restaurants)))
        print(f'\nTIME TO CONNECT RESTAURANTS: {time.time() - start}\n')

    def __create_segment_vertexes(self, segment: Segment):
        vertexes = []
        for coordinate in segment.get_geometry().get_coordinates():
            vertexes.append(Vertex(segment.get_segment_id(), coordinate))
        return vertexes
