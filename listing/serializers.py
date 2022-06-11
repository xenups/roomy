from rest_framework import serializers
from . import models


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ('id', 'rented_by', 'start', 'end')


class RoomSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(many=True)

    class Meta:
        model = models.Room
        fields = ("id", 'room_heading', 'listing', 'reservations')


class ListingSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)

    class Meta:
        model = models.Listing
        fields = ('unit_heading', 'rented_room_count', 'room_count', 'rooms')


class ReserveSerializer(serializers.Serializer):
    name = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    room_id = serializers.IntegerField()
