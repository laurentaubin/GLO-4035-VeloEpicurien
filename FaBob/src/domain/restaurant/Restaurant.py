from domain.Coordinates import Coordinates


class Restaurant:
    def __init__(self, identifier: str, name: str, coordinates: Coordinates, types):
        self.id = identifier
        self.name = name
        self.coordinates = coordinates
        self.types = types

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "coordinates": self.coordinates.to_dict(),
            "types": self.types,
        }
