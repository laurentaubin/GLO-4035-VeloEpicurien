from unittest import TestCase

from api.HeartbeatResource import HeartbeatResource
from api.dto.HeartbeatDto import HeartbeatDto


class TestHeartbeatResource(TestCase):
    A_CITY = "city"

    def setUp(self) -> None:
        self.heartbeat_resource = HeartbeatResource(self.A_CITY)

    def test_givenCity_whenSendHeartbeat_thenReturnHeartbeatDtoWithCity(self):
        expected_heartbeat_dto = HeartbeatDto(self.A_CITY)

        actual_heartbeat_dto = self.heartbeat_resource.send_heartbeat()

        self.assertEqual(
            actual_heartbeat_dto.get_city(), expected_heartbeat_dto.get_city()
        )
