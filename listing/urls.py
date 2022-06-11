from util.url import method_dispatch
from .views import *
from django.urls import path

urlpatterns = [
    path('listings/', get_owner_listings_controller, name='listings'),
    path('reserve/', make_reservation_controller, name='reserve'),
    path('rooms/available/', get_available_rooms_controller, name='reserve'),
    path('menu/', owner_listing_view),
    # path('listing_rooms/', method_dispatch(GET=get_listing_rooms), name='y'),
    # path('available_listings/', method_dispatch(GET=get_available_listings), name='t'),
    # path('available_rooms/', method_dispatch(GET=get_available_rooms_controller), name='t'),

]
