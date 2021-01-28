import typing as tp
import asyncio

from fastapi import APIRouter, Depends

from tortoise.contrib.fastapi import HTTPNotFoundError

from models import profiles, users
from models.cities import City, City_Pydantic
from services.auth import Auth


profile_router = APIRouter()


@profile_router.post('/profile')
async def create_profile(profile: profiles.CreateProfile):
    # print(**profile.dict(exclude_unset=True))
    profile_obj = await profiles.Profile.create(**profile.dict(exclude_unset=True))
    return await profiles.Profile_Pydantic.from_tortoise_orm(profile_obj)


@profile_router.get('/profiles')
async def get_users():
    return await profiles.Profile_Pydantic.from_queryset(profiles.Profile.all())


@profile_router.put('/profile/{profile_id}', response_model=profiles.Profile_Pydantic)
async def update_profile(profile_id: str, profile: profiles.UpdateProfile):
    await profiles.Profile.filter(id=profile_id).update(**profile.dict(exclude_unset=True))
    return await profiles.Profile_Pydantic.from_queryset_single(profiles.Profile.get(id=profile_id))


@profile_router.put('/profile/add-city/{profile_id}', response_model=profiles.Profile_Pydantic)
async def add_profile_city(profile_id: str, cities_data: profiles.ProfileAddCity):
    profile = await profiles.Profile.get(id=profile_id)
    cities_obj = await City.filter(id__in=cities_data.cities)

    await profile.cities.add(*cities_obj)

    profile_obj = await profiles.Profile_Pydantic.from_tortoise_orm(profile)
    return profile_obj


@profile_router.get('/profile/me')
async def get_my_profile(user: users.User_Pydantic = Depends(Auth.get_current_user)):
    profile = await profiles.Profile.get(user=user.id)
    return await profiles.Profile_Pydantic.from_tortoise_orm(profile)


@profile_router.get('/profile/my-cities')
async def get_my_profile(user: users.User_Pydantic = Depends(Auth.get_current_user)):
    profile = await profiles.Profile.get(user=user.id)
    cities = await City_Pydantic.from_queryset(profile.cities.all())
    await City.get_weather_for_cities(cities)
    return cities
