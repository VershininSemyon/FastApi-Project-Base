
from exceptions.base import AppError


class UserError(AppError):
    pass


class UserCreationError(UserError):
    pass


class UsernameAlreadyExistsError(UserCreationError):
    pass


class EmailAlreadyExistsError(UserCreationError):
    pass
