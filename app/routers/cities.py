import asyncio

from fastapi import APIRouter

from models.cities import City, City_Pydantic, CreateCity, City_Pydantic_List

city_router = APIRouter()


@city_router.post('/city', response_model=City_Pydantic)
async def create_city(city: CreateCity):
    city_obj = await City.create(**city.dict(exclude_unset=True))
    return await City_Pydantic.from_tortoise_orm(city_obj)


@city_router.get('/cities', response_model=City_Pydantic_List)
async def get_cities():
    cities = await City_Pydantic.from_queryset(City.all())
    await City.get_weather_for_cities(cities)

    return cities


@city_router.get('/city/{city_id}', response_model=City_Pydantic)
async def get_city(city_id: str):
    city = await City_Pydantic.from_queryset_single(City.get(id=city_id))
    await City.get_weather(city)
    return city
