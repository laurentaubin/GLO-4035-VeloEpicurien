from domain.Coordinate import Coordinate


class Restaurant:
    def __init__(self, identifier: str, name: str, coordinates: Coordinate, types):
        self.__id = identifier
        self.__name = name
        self.__coordinates = coordinates
        self.__types = types

    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "coordinates": self.__coordinates.to_dict(),
            "types": self.__types,
        }