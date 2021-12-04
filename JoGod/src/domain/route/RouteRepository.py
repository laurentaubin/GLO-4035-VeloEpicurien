from typing import List


class RouteRepository:
    def find_route(
        self, starting_point: dict, types: List[str], length: int, number_of_stops: int
    ):
        pass

    def find_starting_point(self, length: int, types: List[str]):
        pass

    def add_types(self):
        pass
