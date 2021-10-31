from domain.restaurant.RestaurantRepository import RestaurantRepository


class RestaurantResource:
    def __init__(self, restaurant_repository: RestaurantRepository):
        self.restaurant_repository = restaurant_repository

    def get_total_number_of_restaurants(self) -> int:
        return self.restaurant_repository.get_total_number_of_restaurants()
