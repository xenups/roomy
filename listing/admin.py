from django.contrib import admin

# Register your models here.
from listing.models import Listing, Room, Reservation

admin.site.register(Listing)
admin.site.register(Room)
admin.site.register(Reservation)
