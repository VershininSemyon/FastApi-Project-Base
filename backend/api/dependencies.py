
from typing import Annotated

from db.database import async_session_factory
from db.unitofwork import UnitOfWork
from fastapi import Depends
from services.user import UserService


def get_uow() -> UnitOfWork:
    return UnitOfWork(async_session_factory)

UOWDep = Annotated[UnitOfWork, Depends(get_uow)]

def get_user_service(uow: UOWDep) -> UserService:
    return UserService(uow)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
