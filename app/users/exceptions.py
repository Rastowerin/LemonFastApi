from app.exceptions import BadRequestException


class UserNotFoundException(BadRequestException):
    status = 404


class InvalidCredentialsException(BadRequestException):
    status = 400


class UserAlreadyExistsException(BadRequestException):
    status = 409
