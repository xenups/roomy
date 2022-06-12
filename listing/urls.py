from util.url import method_dispatch
from .views import *
from django.urls import path

urlpatterns = [
    path('listings/', get_owner_listings_controller, name='listings'),
    path('reserve/', make_reservation_controller, name='reserve'),
    path('rooms/available/', get_available_rooms_controller, name='available'),
    path('manager/', owner_listing_view),
]
