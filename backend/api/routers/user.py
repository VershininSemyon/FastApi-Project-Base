
from api.dependencies import UserServiceDep, CurrentUserDep
from fastapi import APIRouter, status
from schemas.user import UserCreateSchema, UserReadSchema

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post(
    "/", 
    response_model=UserReadSchema, 
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreateSchema,
    user_service: UserServiceDep
):
    new_user = await user_service.create_user(user_data)
    return new_user


@user_router.get(
    "/me",
    response_model=UserReadSchema,
    status_code=status.HTTP_200_OK,
)
async def get_me(
    current_user: CurrentUserDep,
) -> UserReadSchema:
    return current_user
