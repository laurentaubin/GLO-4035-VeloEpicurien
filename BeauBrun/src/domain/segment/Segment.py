class Segment:
    def __init__(self, id: str, length: float, geometry: SegmentGeometry, name: str):
        self.id = id
        self.length = length
        self.geometry = geometry
        self.name = name