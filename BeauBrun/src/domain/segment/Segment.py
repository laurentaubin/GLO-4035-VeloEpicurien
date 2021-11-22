from domain.segment.SegmentGeometry import SegmentGeometry


class Segment:
    def __init__(self, id: str, length: float, geometry: SegmentGeometry, name: str):
        self.__id = id
        self.__length = length
        self.__geometry = geometry
        self.__name = name

    def get_id(self) -> str:
        return self.__id

    def get_geometry(self) -> SegmentGeometry:
        return self.__geometry
