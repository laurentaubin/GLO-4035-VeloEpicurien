from api.dto.HeartbeatDto import HeartbeatDto


class HeartbeatResource:
    def __init__(self, chosen_city: str) -> None:
        self.__chosen_city = chosen_city

    def send_heartbeat(self) -> HeartbeatDto:
        return HeartbeatDto(self.__chosen_city)
