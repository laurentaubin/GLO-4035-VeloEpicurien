from typing import List

from domain.Coordinate import Coordinate


class Restaurant:
    def __init__(self, identifier: str, name: str, coordinates: Coordinate, types: List[str], near_segments: List[str]):
        self.__id = identifier
        self.__name = name
        self.__coordinates = coordinates
        self.__types = types
        self.__near_segments = near_segments

    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "coordinates": self.__coordinates.to_dict(),
            "types": self.__types,
        }

    def get_id(self) -> str:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_types(self) -> List[str]:
        return self.__types

    def get_coordinates(self) -> Coordinate:
        return self.__coordinates

    def get_near_segments(self) -> List[str]:
        return self.__near_segments
