from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.SegmentRepository import SegmentRepository


class TransformedDataResource:
    def __init__(self, segment_repository: SegmentRepository, restaurant_repository: RestaurantRepository):
        self.__segment_repository = segment_repository
        self.__restaurant_repository = restaurant_repository

    def get_transformed_data(self) -> dict:
        return {
            "restaurants": self.__restaurant_repository.get_number_of_restaurants_per_type(),
            "longueurCyclable": self.__segment_repository.get_total_segment_length(),
        }
