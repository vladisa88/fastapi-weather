import os
import asyncio
import aiohttp

import pytemperature


token = os.environ.get('OPEN_WEATHER_API_KEY')
base_url = 'https://api.openweathermap.org/data/2.5/' \
            'weather?q={city}&appid={token}'


async def get_current_weather(city: str) -> str:
    url = base_url.format(
        city=city,
        token=token
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


def converter(temperature: float) -> float:
    return round(pytemperature.k2c(temperature), 2)
