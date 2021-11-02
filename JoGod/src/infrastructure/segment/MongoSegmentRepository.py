from pymongo import MongoClient

from domain.segment.SegmentRepository import SegmentRepository


class MongoSegmentRepository(SegmentRepository):
    def __init__(self, mongo_address: str) -> None:
        self.__mongo_client = MongoClient(mongo_address)
        self.__segments_database = self.__mongo_client.epicurien
        self.__segments_collection = self.__segments_database["segments"]

    def get_total_number_of_segments(self):
        return self.__segments_collection.find().count()

    def get_total_segment_length(self):
        cursor = self.__segments_collection.aggregate(
            [{"$group": {"_id": "null", "total": {"$sum": "$length"}}}]
        )
        results = [doc for doc in cursor]
        return results[0].get("total")
