class Coordinate:
    def __init__(self, latitude: float, longitude: float) -> None:
        self.__latitude = latitude
        self.__longitude = longitude

    def get_latitude(self) -> float:
        return self.__latitude

    def get_longitude(self) -> float:
        return self.__longitude

    def to_dict(self):
        return {"latitude": self.__latitude, "longitude": self.__longitude}
