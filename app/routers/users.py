import typing as tp

from fastapi import APIRouter, Depends

from models import users
from services.auth import Auth


user_router = APIRouter()


@user_router.get('/users')
async def get_users(email: tp.Optional[str] = None):
    if email:
        return await users.User_Pydantic.from_queryset_single(users.UserModel.get(email=email))
    users_obj = await users.UserModel.all()
    for user in users_obj:
        print(user.id)
    return await users.User_Pydantic.from_queryset(users.UserModel.all())


@user_router.get('/users/me', response_model=users.User_Pydantic)
async def get_user(user: users.User_Pydantic = Depends(Auth.get_current_user)):
    # print(user.profile)
    return user