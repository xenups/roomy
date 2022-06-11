from datetime import timedelta

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime

from listing.Domains.listing_domains import ReservationRequest, AvailableRoomRequest
from listing.repositories.listing_repository import RoomRepository, ListingRepository, ReservationRepository


class ServiceResponse:
    def __init__(self, successful, response=None, status=503):
        self.successful = successful
        self.response = response
        self.status = status


class RoomService(object):
    def __init__(self):
        self.roomRepository = RoomRepository()

    def get_available(self, available_room_req: AvailableRoomRequest):
        date = parse_datetime(available_room_req.date)
        room = self.roomRepository.get_available(date)
        response = ServiceResponse(response=room, successful=True)
        return response


class ReservationService(object):
    def __init__(self):
        self.reservation_repository = ReservationRepository()

    def reserve(self, reservation_req: ReservationRequest):
        reservation = self.reservation_repository.get_last_one(reservation_req.room_id)
        reservation_time_req = parse_datetime(reservation_req.start)
        try:
            if reservation is None or reservation_time_req > reservation.end + timedelta(hours=8):
                reservation = self.reservation_repository.create(reservation_req)
                return ServiceResponse(response=reservation, successful=True, status=200)
            return ServiceResponse(response="room is full", successful=False, status=409)
        except Exception as e:
            return ServiceResponse(response=e.args, successful=False, status=503)


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
            print(e)
            return ServiceResponse(successful=False)
