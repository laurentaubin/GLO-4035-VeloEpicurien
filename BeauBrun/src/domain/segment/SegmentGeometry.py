from domain.segment.SegmentCoordinates import SegmentCoordinates


class SegmentGeometry:
    def __init__(self, type: str, coordinates: SegmentCoordinates):
        self.__type = type
        self.__coordinates = coordinates
