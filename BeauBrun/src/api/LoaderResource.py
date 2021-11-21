from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.SegmentRepository import SegmentRepository
from service.GraphService import GraphService


class LoaderResource:
    def __init__(
        self,
        graph_service: GraphService
    ) -> None:
        self.__graph_service = graph_service

    def load_segments(self):
        self.__graph_service.load_segments()

    def connect_near_segments_together(self):
        self.__graph_service.connect_near_segments_together()

    def connect_restaurants_to_segments(self):
        self.__graph_service.connect_restaurants_to_segments()

