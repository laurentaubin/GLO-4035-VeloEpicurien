import time

from domain.restaurant.RestaurantRepository import RestaurantRepository
from domain.segment.SegmentRepository import SegmentRepository


class ConnectorService:
    def __init__(self, restaurant_repository: RestaurantRepository, segment_repository: SegmentRepository):
        self.__restaurant_repository = restaurant_repository
        self.__segment_repository = segment_repository

    def connect_near_restaurants_to_segments(self):
        print("\nLINKING NEAR SEGMENTS TO RESTAURANTS")
        start = time.time()
        restaurants = self.__restaurant_repository.find_all()
        print("\nNUMBER OF RESTAURANTS: ", len(restaurants))
        number_of_restaurants_not_near_any_segment = 0
        for restaurant in restaurants:
            segments_near_to_restaurant = self.__segment_repository.find_near_segments(restaurant.get_coordinates())
            print(segments_near_to_restaurant)
            if len(segments_near_to_restaurant) == 0:
                number_of_restaurants_not_near_any_segment += 1
            restaurant.set_near_segments(segments_near_to_restaurant)
            self.__restaurant_repository.update(restaurant)
        print("\n NUMBER OF RESTAURANTS NOT NEAR ANY SEGMENT: ", number_of_restaurants_not_near_any_segment)
        print(f'\nTIME TO LINK NEAR SEGMENTS TO RESTAURANTS : {time.time() - start}')
