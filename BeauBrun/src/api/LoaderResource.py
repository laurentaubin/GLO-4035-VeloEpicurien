from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.SegmentRepository import SegmentRepository
from service.GraphService import GraphService


class LoaderResource:
    def __init__(self, graph_service: GraphService) -> None:
        self.__graph_service = graph_service

    def load_segments(self):
        print("\nCALL TO LOAD SEGMENT RECEIVED\n")
        self.__graph_service.load_segments()
        self.__graph_service.connect_near_segments_together()
        self.__graph_service.connect_restaurants_to_segments()
        return "OK"
