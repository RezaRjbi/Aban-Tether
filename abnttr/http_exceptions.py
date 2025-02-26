from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    status_code = 400
    default_code = "bad_request"
    default_detail = "Bad Request"


class UnauthorizedException(APIException):
    status_code = 401
    default_code = "unauthorized"
    default_detail = "Unauthorized"


class ForbiddenException(APIException):
    status_code = 403
    default_code = "access_denied"
    default_detail = "Access desnied"


class TooManyRequestsException(APIException):
    status_code = 429
    default_code = "too_many_requests"
    default_detail = "Too Many Requests"
