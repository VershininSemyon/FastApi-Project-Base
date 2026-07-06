
from db.unitofwork import UnitOfWork
from exceptions.auth import (InvalidPasswordError, InvalidTokenTypeError,
                             UserNotFoundError)
from exceptions.user import EmailAlreadyExistsError, UsernameAlreadyExistsError
from integrations.jwt_auth import (create_access_token, create_refresh_token,
                                   decode_token)
from schemas.auth import JWTTokenPairResponseSchema, UserLoginSchema
from schemas.user import UserCreateSchema, UserReadSchema, UserUpdateSchema


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    async def create_user(self, data: UserCreateSchema) -> UserReadSchema:
        async with self.uow:
            user = await self.uow.user_repository.get_by_username(data.username)
            if user is not None:
                raise UsernameAlreadyExistsError()
            
            user = await self.uow.user_repository.get_by_email(data.email)
            if user is not None:
                raise EmailAlreadyExistsError()
            
            created_user = await self.uow.user_repository.create(data.model_dump())
            await self.uow.commit()
        
        return UserReadSchema.model_validate(created_user)
    
    async def get_tokens(self, login_data: UserLoginSchema) -> JWTTokenPairResponseSchema:
        async with self.uow:
            user = await self.uow.user_repository.get_by_username(login_data.username)
        
        if not user:
            raise UserNotFoundError()
        
        if user.password != login_data.password:
            raise InvalidPasswordError()
        
        user_data = {
            "username": user.username,
            "email": user.email
        }

        return JWTTokenPairResponseSchema.model_validate({
            "access": create_access_token(user_data),
            "refresh": create_refresh_token(user_data)
        })
    
    def refresh_token(self, refresh_token: str) -> str:
        data = decode_token(refresh_token)
        user_data = {
            "username": data['username'],
            "email": data['email']
        }

        access = create_access_token(user_data)
        return access

    async def authenticate_user(self, access_token: str):
        data = decode_token(access_token)

        if data['token_type'] != 'access':
            raise InvalidTokenTypeError()

        async with self.uow:
            user = await self.uow.user_repository.get_by_username(data['username'])
            return UserReadSchema.model_validate(user)

    async def delete_user(self, user_id: str) -> None:
        async with self.uow:
            await self.uow.user_repository.delete(user_id)
