from domain.segment.SegmentRepository import SegmentRepository


class SegmentResource:
    def __init__(self, segment_repository: SegmentRepository):
        self.segment_repository = segment_repository

    def get_total_number_of_segments(self):
        return self.segment_repository.get_total_number_of_segments()

    def get_total_segment_length(self):
        return self.segment_repository.get_total_segment_length()