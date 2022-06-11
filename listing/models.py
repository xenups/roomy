from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Listing(models.Model):
    unit_heading = models.CharField(max_length=50, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owners')
    description = models.CharField(max_length=1024)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.unit_heading

    @property
    def rented_room_count(self):
        return self.rooms.filter(reservations__end__gt=timezone.now()).count()

    @property
    def room_count(self):
        return self.rooms.count()


class Room(models.Model):
    room_heading = models.CharField(max_length=50, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='rooms')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room_heading


class Reservation(models.Model):
    rented_by = models.CharField(max_length=250, blank=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='reservations')
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.room.room_heading + " rented by " + self.rented_by
