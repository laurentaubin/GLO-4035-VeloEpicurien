from domain.Coordinate import Coordinate


class Vertex:
    def __init__(self, id: str, coordinate: Coordinate):
        self.__id = id
        self.__coordinate = coordinate

    def get_id(self) -> str:
        return self.__id

    def get_coordinate(self) -> Coordinate:
        return self.__coordinate
