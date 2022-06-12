from dacite import from_dict
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .Domains.listing_domains import ReservationRequest, AvailableRoomRequest
from .Services.listing_services import RoomService, ListingService, ReservationService
from .serializers import ListingSerializer, RoomSerializer, ReserveSerializer, ReservationSerializer


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_owner_listings_controller(request):
    listing_response = ListingService().get_owners_listing(username=request.GET.get("username"))
    if listing_response.successful:
        serializer = ListingSerializer(listing_response.response, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(data=listing_response.response, status=listing_response.state)


@api_view(["POST"])
@permission_classes((AllowAny,))
def make_reservation_controller(request):
    serializer = ReserveSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    req = from_dict(data_class=ReservationRequest, data=serializer.data)
    service_response = ReservationService().reserve(req)
    if service_response.successful:
        room_data = ReservationSerializer(service_response.response)
        return Response(room_data.data, status=status.HTTP_200_OK)
    return Response(data=service_response.response, status=service_response.state)


@api_view(["GET"])
@permission_classes((AllowAny,))
def get_available_rooms_controller(request):
    start = request.GET.get("start")
    end = request.GET.get("end")
    req = AvailableRoomRequest(start=start, end=end)
    service_response = RoomService().get_available(req)
    if service_response.successful:
        serializer = RoomSerializer(service_response.response, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(data=service_response.response, status=service_response.state)


def owner_listing_view(request):
    username = request.GET.get("username")
    listing_response = ListingService().get_owners_listing(username=username)
    context = {
        "list": listing_response.response,
    }
    return render(request, "table.html", context)
