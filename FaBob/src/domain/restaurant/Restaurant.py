from typing import List

from domain.Coordinates import Coordinates


class Restaurant:
    def __init__(
        self, identifier: str, name: str, coordinates: Coordinates, types: List[str]
    ):
        self.__id = identifier
        self.__name = name
        self.__coordinates = coordinates
        self.__types = types
        self.__geometry = {}
        self.__near_segments = []

    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "coordinates": self.__coordinates.to_dict(),
            "types": self.__types,
            "geometry": self.__geometry,
            "near_segments": self.__near_segments,
        }

    def get_id(self) -> str:
        return self.__id

    def get_coordinates(self):
        return self.__coordinates

    def set_geometry(self, geometry):
        self.__geometry = geometry

    def get_near_segments(self) -> List[str]:
        return self.__near_segments

    def set_near_segments(self, near_segments: List[str]):
        self.__near_segments = near_segments
