from datetime import timedelta

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime

from listing.Domains.listing_domains import ReservationRequest, AvailableRoomRequest
from listing.repositories.listing_repository import RoomRepository, ListingRepository, ReservationRepository


class ServiceState:
    RoomIsFull = 409
    Reserved = 200
    Unavailable = 503


class ServiceResponse:
    def __init__(self, successful, response=None, status=503):
        self.successful = successful
        self.response = response
        self.state = status


class RoomService(object):
    def __init__(self):
        self.roomRepository = RoomRepository()

    def get_available(self, available_room_req: AvailableRoomRequest):
        start = parse_datetime(available_room_req.start)
        end = parse_datetime(available_room_req.end)
        room = self.roomRepository.get_available(start=start, end=end)
        response = ServiceResponse(response=room, successful=True)
        return response


class ReservationService(object):
    def __init__(self):
        self.reservation_repository = ReservationRepository()

    def reserve(self, reservation_req: ReservationRequest):
        try:
            if self.reservation_repository.is_available(reservation_req.room_id, parse_datetime(reservation_req.start),
                                                        parse_datetime(reservation_req.end)):
                reservation = self.reservation_repository.create(reservation_req)
                return ServiceResponse(response=reservation, successful=True, status=ServiceState.Reserved)
            return ServiceResponse(response={"detail": "room is full"}, successful=False,
                                   status=ServiceState.RoomIsFull)
        except Exception as e:
            return ServiceResponse(response=e.args[0], successful=False, status=ServiceState.Unavailable)


class ListingService(object):
    def __init__(self):
        self.repository = ListingRepository()

    def get_owners_listing(self, username):
        user = get_object_or_404(User, username=username)
        try:
            listings = self.repository.get_owner_listing(user)
            response = ServiceResponse(response=listings, successful=True)
            return response
        except Exception as e:
            return ServiceResponse(response=e.args[0], successful=False)
