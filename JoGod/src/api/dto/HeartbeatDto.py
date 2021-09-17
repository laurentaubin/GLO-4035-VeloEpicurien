class HeartbeatDto:
    def __init__(self, city: str) -> None:
        self.__city = city

    def get_city(self) -> str:
        return self.__city

    def to_dict(self) -> dict:
        return {
            "villeChoisie": self.__city
        }
