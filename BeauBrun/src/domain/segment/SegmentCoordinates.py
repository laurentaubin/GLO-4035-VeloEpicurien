from typing import List

from domain.Coordinate import Coordinate


class SegmentCoordinates:
    def __init__(self, segment_coordinates: List[Coordinate]):
        self.__segment_coordinates = segment_coordinates

    def get_coordinates(self):
        return self.__segment_coordinates
