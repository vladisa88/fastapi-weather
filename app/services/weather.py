import asyncio
import aiohttp

import pytemperature


token = 'a0337f8161e5015e69d7ea72df5e8e2c'
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
