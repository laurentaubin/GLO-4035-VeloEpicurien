import json
from typing import List

from domain.segment.SegmentRepository import SegmentRepository
from pymongo import MongoClient


class MongoSegmentRepository(SegmentRepository):
    def __init__(self, mongo_address: str, segment_data_filepath: str) -> None:
        self.__mongo_client = MongoClient(mongo_address)
        self.__segment_data_filepath = segment_data_filepath
        self.__segments_database = self.__mongo_client.epicurien
        self.__segments_collection = self.__segments_database["segments"]
        self.__segments_collection.remove({})

    def load_segments(self) -> None:
        segments = self.__read_segment_data_file()
        self.__segments_collection.insert_many(segments)

    def __read_segment_data_file(self) -> List[dict]:
        with open(self.__segment_data_filepath) as segment_data_file:
            segment_raw_data = json.load(segment_data_file).get("features")
            segments = []
            for raw_segment in segment_raw_data:
                segments.append(self.__assemble_segment(raw_segment))
            return segments

    def __assemble_segment(self, segment_data_entry) -> dict:
        geometry = segment_data_entry["geometry"]
        length: str = segment_data_entry["properties"]["LONGUEUR"]
        name: str = segment_data_entry["properties"]["NOM_TOPOGRAPHIE"]
        return {"geometry": geometry, "length": length, "name": name}
