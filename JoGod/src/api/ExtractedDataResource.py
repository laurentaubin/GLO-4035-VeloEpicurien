from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.SegmentRepository import SegmentRepository


class ExtractedDataResource:
    def __init__(
        self,
        segment_repository: SegmentRepository,
        restaurant_repository: RestaurantRepository,
    ):
        self.__segment_repository = segment_repository
        self.__restaurant_repository = restaurant_repository

    def get_extracted_data(self) -> dict:
        return {
            "nbRestaurants": self.__restaurant_repository.get_total_number_of_restaurants(),
            "nbSegments": self.__segment_repository.get_total_number_of_segments(),
        }
