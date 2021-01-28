import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from config.db import DB_CONFIG
from config.settings import Settings

from routers.auth import auth_router
from routers.users import user_router
from routers.profiles import profile_router
from routers.cities import city_router

settings = Settings()
app = FastAPI(title=settings.APP_NAME)

app.include_router(
    auth_router,
    prefix=settings.API_PREFIX + '/auth',
    tags=['Authentication']
)

app.include_router(
    user_router,
    prefix=settings.API_PREFIX,
    tags=['Users']
)

app.include_router(
    profile_router,
    prefix=settings.API_PREFIX,
    tags=['Profiles']
)

app.include_router(
    city_router,
    prefix=settings.API_PREFIX,
    tags=['Cities']
)

register_tortoise(
    app,
    config=DB_CONFIG,
    generate_schemas=True,
)


if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=True)
