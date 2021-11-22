from typing import List

from domain.Coordinate import Coordinate
from domain.segment.SegmentCoordinates import SegmentCoordinates


class SegmentGeometry:
    def __init__(self, type: str, coordinates: SegmentCoordinates):
        self.__type = type
        self.__coordinates = coordinates

    def get_coordinates(self) -> List[Coordinate]:
        return self.__coordinates.get_coordinates()
