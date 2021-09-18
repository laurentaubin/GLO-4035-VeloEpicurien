from unittest import TestCase

from api.HeartbeatResource import HeartbeatResource


class TestHeartbeatResource(TestCase):
    A_CITY = "city"

    def setUp(self) -> None:
        self.heartbeat_resource = HeartbeatResource(self.A_CITY)

    def test_givenCity_whenSendHeartbeat_thenReturnHeartbeatDtoWithCity(self):
        actual_heartbeat_dto = self.heartbeat_resource.send_heartbeat()

        self.assertEqual(
            actual_heartbeat_dto.get_city(), self.A_CITY
        )
