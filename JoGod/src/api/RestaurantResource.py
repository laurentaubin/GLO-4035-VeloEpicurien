from domain.restaurant.RestaurantRepository import RestaurantRepository


class RestaurantResource:
    def __init__(self, restaurant_repository: RestaurantRepository):
        self.__restaurant_repository = restaurant_repository

    def get_total_number_of_restaurants(self) -> int:
        return self.__restaurant_repository.get_total_number_of_restaurants()

    def get_number_of_restaurants_per_type(self) -> dict:
        return self.__restaurant_repository.get_number_of_restaurants_per_type()
