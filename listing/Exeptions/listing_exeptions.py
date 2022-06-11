from rest_framework import status
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'


class ApiException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'something wrong happened'

    def __init__(self, detail, status_code=200):
        self.status_code = status_code
        self.detail = detail
