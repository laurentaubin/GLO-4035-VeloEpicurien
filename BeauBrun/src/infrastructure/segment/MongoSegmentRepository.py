import json
from typing import List

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

    def find_all(self) -> List[dict]:
        pass

    def __assemble_segment(self, segment_data_entry) -> Segment:
        segment_coordinates = SegmentCoordinates(segment_data_entry["geometry"]["coordinates"])
        geometry_type: str = segment_data_entry["geometry"]["type"]
        geometry = SegmentGeometry(geometry_type, segment_coordinates)
        length: float = segment_data_entry["properties"]["LONGUEUR"]
        name: str = segment_data_entry["properties"]["NOM_TOPOGRAPHIE"]
        id: str = "anId"
        return Segment(id, length, geometry, name)
