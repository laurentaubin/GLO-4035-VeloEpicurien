from typing import List

from domain.restaurant.Restaurant import Restaurant


class RestaurantRepository:
    def find_all(self) -> List[Restaurant]:
        pass

    def update(self, restaurant: Restaurant):
        pass

    def load_restaurants(self) -> None:
        pass
