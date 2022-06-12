from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.datetime_safe import datetime

from ..Domains.listing_domains import ReservationRequest
from ..models import Listing, Room, Reservation


def listing_rooms(listing_id=1):
    return Room.objects.filter(rental_unit_id=listing_id).all()


def get_available_listing():
    return Listing.objects.filter(rooms__is_rented=False).all()


class RoomRepository:
    def __init__(self):
        self.room = Room

    def get(self, pk: int):
        return get_object_or_404(self.room, id=pk)

    def list(self):
        return self.room.objects.all()

    def get_available(self, date):
        return self.room.objects.filter(Q(reservations__end__lt=date) | Q(reservations__isnull=True)).all()


class ListingRepository:
    def __init__(self):
        self.Listing = Listing

    def get_owner_listing(self, owner):
        return self.Listing.objects.filter(owner=owner)

    def get(self, pk: int):
        return get_object_or_404(self.Listing, pk=pk)

    def list(self):
        return self.Listing.objects.all()


class ReservationRepository:
    def __init__(self):
        self.reservation = Reservation
        self.room = Room

    def create(self, reservation_req: ReservationRequest):
        reservation = Reservation()
        reservation.room = get_object_or_404(self.room, id=reservation_req.room_id)
        reservation.start = reservation_req.start
        reservation.end = reservation_req.end
        reservation.rented_by = reservation_req.name
        reservation.save()
        return reservation

    def get(self, pk: int):
        return get_object_or_404(self.reservation, id=pk)

    def get_last_one(self, room_id):
        try:
            return self.reservation.objects.filter(room_id=room_id).last()
        except Listing.DoesNotExist:
            return None

    def is_available(self, start, end):
        if self.reservation.objects.filter(start__lte=end, end__gte=start).first():
            return False
        return True

    def list(self):
        return self.reservation.objects.all()
