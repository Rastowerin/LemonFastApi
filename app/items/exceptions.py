from app.exceptions import BadRequestException


class ItemNotFoundException(BadRequestException):
    status = 404


class ItemAlreadyExistsException(BadRequestException):
    status = 409
