from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.SegmentRepository import SegmentRepository


class LoaderResource:
    def __init__(
        self,
        restaurant_repository: RestaurantRepository,
        segment_repository: SegmentRepository,
    ) -> None:
        self.restaurant_repository = restaurant_repository
        self.segment_repository = segment_repository

    def load_restaurants(self) -> None:
        self.restaurant_repository.load_restaurants()
        self.segment_repository.load_segments()
