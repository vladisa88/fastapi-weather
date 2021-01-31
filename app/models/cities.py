import asyncio

from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)

from pydantic import BaseModel

from services.weather import get_current_weather, converter
from config.settings import get_settings

settings = get_settings()

class City(models.Model):
    title = fields.CharField(max_length=50, unique=True)

    def weather(self) -> str:
        return ''

    @classmethod
    async def get_weather(cls, obj) -> str:
        weather = await get_current_weather(obj.title)
        obj.weather = converter(weather['main']['temp'])

    @staticmethod
    async def get_weather_for_cities(cities: list) -> None:
        tasks = []
        for city in cities:
            task = asyncio.create_task(City.get_weather(city))
            tasks.append(task)

        await asyncio.gather(*tasks)

    class PydanticMeta:
        computed = ('weather', )


class CreateCity(BaseModel):
    title: str


class CityAll(BaseModel):
    id: int
    title: str

Tortoise.init_models(settings.MODELS, 'models')

City_Pydantic = pydantic_model_creator(
    City,
    name='City'
)
CityIn_Pydantic = pydantic_model_creator(
    City,
    name='City',
    exclude_readonly=True
)

City_Pydantic_List = pydantic_queryset_creator(City)
