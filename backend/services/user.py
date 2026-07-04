
from db.unitofwork import UnitOfWork
from schemas.user import UserCreateSchema, UserReadSchema
from exceptions.user import UsernameAlreadyExistsError, EmailAlreadyExistsError


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def create_user(self, data: UserCreateSchema) -> UserReadSchema:
        async with self.uow:
            user = await self.uow.user_repository.get_by_username(data.username)
            if user is not None:
                raise UsernameAlreadyExistsError("Пользователь с таким username уже есть!")

            user = await self.uow.user_repository.get_by_email(data.email)
            if user is not None:
                raise EmailAlreadyExistsError("Пользователь с таким email уже есть!")

            created_user = await self.uow.user_repository.create(data.model_dump())
            await self.uow.commit()
        
        return UserReadSchema.model_validate(created_user)
