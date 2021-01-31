import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    USER: str = os.environ.get('POSTGRES_USER')
    PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')
    DB_HOST: str = os.environ.get('POSTGRES_HOST')
    DB_PORT: str = os.environ.get('POSTGRES_PORT')
    DATABASE_NAME: str = os.environ.get('POSTGRES_DB')
    DATABASE_URL: str = f'postgres://{USER}:{PASSWORD}@{DB_HOST}:'\
                        f'{DB_PORT}/{DATABASE_NAME}'
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    APP_NAME: str = 'Weather App'
    REGISTRATION_TOKEN_LIFETIME: int = 60 * 60
    TOKEN_ALGORITHM: str = 'HS256'
    SMTP_SERVER: str = 'localhost:25'
    MAIL_SENDER = 'noreply@example.com'
    API_PREFIX = '/api'
    HOST = os.environ.get('BACK_END_HOST', '0.0.0.0')
    PORT = int(os.environ.get('BACK_END_PORT'))
    BASE_URL = '{}:{}/'.format(HOST, str(PORT))
    MODELS = [
        'models.users',
        'models.profiles',
        'models.cities',
        'aerich.models'
    ]

    class Config:
        case_sensitive: bool = True


@lru_cache
def get_settings():
    return Settings()
