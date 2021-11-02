from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.SegmentRepository import SegmentRepository


class LoaderResource:
    def __init__(
        self,
        restaurant_repository: RestaurantRepository,
        segment_repository: SegmentRepository,
    ) -> None:
        self.__restaurant_repository = restaurant_repository
        self.__segment_repository = segment_repository

    def load_restaurants(self) -> None:
        self.__restaurant_repository.load_restaurants()

    def load_segments(self) -> None:
        self.__segment_repository.load_segments()
