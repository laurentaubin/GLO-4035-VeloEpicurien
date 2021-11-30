import json
import time
from typing import List

from domain.Coordinate import Coordinate
from domain.segment.Segment import Segment
from domain.segment.SegmentCoordinates import SegmentCoordinates
from domain.segment.SegmentGeometry import SegmentGeometry
from domain.segment.SegmentRepository import SegmentRepository
from pymongo import MongoClient


class MongoSegmentRepository(SegmentRepository):
    def __init__(self, mongo_address: str) -> None:
        self.__mongo_client = MongoClient(mongo_address)
        self.__segments_database = self.__mongo_client.epicurien
        self.__segments_collection = self.__segments_database["segments"]

    def find_all(self) -> List[Segment]:
        segment_documents = self.__segments_collection.find()
        segments = []
        for segment_document in segment_documents:
            segments.append(self.__assemble_segment(segment_document))
        return segments

    def __assemble_segment(self, segment_document) -> Segment:
        geometry = segment_document["geometry"]
        segment_geometry = SegmentGeometry(
            geometry["type"],
            SegmentCoordinates(
                self.__assemble_coordinates(segment_document["geometry"]["coordinates"])
            ),
        )
        length: float = segment_document["length"]
        name: str = segment_document["name"]
        segment_id: str = segment_document["segment_id"]
        near_segments: List[str] = segment_document["near_segments"]
        return Segment(segment_id, length, segment_geometry, name, near_segments)

    def __assemble_coordinates(
        self, raw_coordinates: List[List[float]]
    ) -> List[Coordinate]:
        coordinates = []
        for raw_coordinate in raw_coordinates:
            coordinates.append(Coordinate(raw_coordinate[1], raw_coordinate[0]))
        return coordinates
