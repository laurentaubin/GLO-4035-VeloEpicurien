from typing import List

from domain.segment.SegmentGeometry import SegmentGeometry


class Segment:
    def __init__(
        self,
        segment_id: str,
        length: float,
        geometry: SegmentGeometry,
        name: str,
        near_segments: List[str],
    ):
        self.__segment_id = segment_id
        self.__length = length
        self.__geometry = geometry
        self.__name = name
        self.__near_segments = near_segments

    def get_segment_id(self) -> str:
        return self.__segment_id

    def get_geometry(self) -> SegmentGeometry:
        return self.__geometry

    def get_near_segments(self) -> List[str]:
        return self.__near_segments
