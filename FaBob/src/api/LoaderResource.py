from domain.RestaurantRepository import RestaurantRepository


class LoaderResource:
    def __init__(self, restaurant_repository: RestaurantRepository) -> None:
        self.restaurant_repository: RestaurantRepository = restaurant_repository

    def load_restaurants(self) -> None:
        self.restaurant_repository.load_restaurants()
