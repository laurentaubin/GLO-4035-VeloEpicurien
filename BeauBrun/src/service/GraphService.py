from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.SegmentRepository import SegmentRepository
from infrastructure.graph.NeoGraphRepository import NeoGraphRepository


class GraphService:
    def __init__(self, graph_repository: NeoGraphRepository, segment_repository: SegmentRepository,
                 restaurant_repository: RestaurantRepository):
        self.__graph_repository = graph_repository
        self.__segment_repository = segment_repository
        self.__restaurant_repository = restaurant_repository

    def load_segments(self) -> None:
        segments = self.__segment_repository.find_all()

    def connect_near_segments_together(self) -> None:
        pass

    def connect_restaurants_to_segments(self) -> None:
        pass
