import json
from typing import List

import pymongo

from domain.Coordinates import Coordinates
from domain.segment.SegmentRepository import SegmentRepository
from pymongo import MongoClient


class MongoSegmentRepository(SegmentRepository):
    def __init__(self, mongo_address: str, segment_data_filepath: str) -> None:
        self.__mongo_client = MongoClient(mongo_address)
        self.__segment_data_filepath = segment_data_filepath
        self.__segments_database = self.__mongo_client.epicurien
        self.__segments_collection = self.__segments_database["segments"]
        # self.__segments_collection.remove({})
        self.__segments_collection.create_index(
            [("geometry", "2dsphere")], name="geometry"
        )

    def load_segments(self) -> None:
        number_of_duplicate = 0
        segments = self.__read_segment_data_file()
        self.__segments_collection.insert_many(segments)
        for segment in segments:
            near_segments = set()
            for coordinates in segment["geometry"]["coordinates"]:
                near_segments_doc = self.__segments_collection.find(
                    {
                        "geometry": {
                            "$nearSphere": {
                                "$geometry": {
                                    "type": "Point",
                                    "coordinates": coordinates,
                                },
                                "$maxDistance": 10,
                            }
                        }
                    }
                )
                for near_segment in near_segments_doc:
                    if near_segment["segment_id"] != segment["segment_id"]:
                        near_segments.add(near_segment["segment_id"])
                    else:
                        number_of_duplicate += 1
            near_segments = list(near_segments)
            segment["near_segments"] = near_segments
            self.__segments_collection.update_one(
                {"segment_id": segment["segment_id"]},
                {"$set": {"near_segments": near_segments}},
                upsert=False,
            )
        print("\n DONE LOADING SEGMENTS MONGO \n")

    def find_near_segments(self, coordinates: Coordinates) -> List[str]:
        near_segments = set()
        near_segments_doc = self.__segments_collection.find(
            {
                "geometry": {
                    "$nearSphere": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": [
                                coordinates.get_longitude(),
                                coordinates.get_latitude(),
                            ],
                        },
                        "$maxDistance": 250,
                    }
                }
            }
        )

        for near_segment in near_segments_doc:
            near_segments.add(near_segment["segment_id"])
            break
        near_segments = list(near_segments)
        return near_segments

    def __read_segment_data_file(self) -> List[dict]:
        with open(self.__segment_data_filepath) as segment_data_file:
            segment_raw_data = json.load(segment_data_file).get("features")
            segments = []
            for raw_segment in segment_raw_data:
                segments.append(self.__assemble_segment(raw_segment))
            return segments

    def __assemble_segment(self, segment_data_entry) -> dict:
        segment_id = str(segment_data_entry["properties"]["ID"])
        geometry = segment_data_entry["geometry"]
        length: str = segment_data_entry["properties"]["LONGUEUR"]
        name: str = segment_data_entry["properties"]["NOM_TOPOGRAPHIE"]
        return {
            "segment_id": segment_id,
            "geometry": geometry,
            "length": length,
            "name": name,
            "near_segments": [],
        }