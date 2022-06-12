import dataclasses


@dataclasses.dataclass
class ReservationRequest:
    name: str
    room_id: int
    start: str
    end: str


@dataclasses.dataclass
class AvailableRoomRequest:
    start: str
    end: str
