from django.utils.dateparse import parse_datetime
from rest_framework import serializers
from . import models


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ('id', 'rented_by', 'start', 'end')

    def validate(self, data):
        if parse_datetime(data['start']) > parse_datetime(data['end']):
            raise serializers.ValidationError("end must occur after start")
        return data


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
