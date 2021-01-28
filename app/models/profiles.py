from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from pydantic import BaseModel

from models.cities import CreateCity
from config.settings import get_settings

from services.weather import get_current_weather

settings = get_settings()

class Profile(models.Model):
    user = fields.OneToOneField('models.UserModel', related_name='profile')
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    cities = fields.ManyToManyField('models.City', related_name='profiles')

    class PydanticMeta:
        exclude = (
            'id',
            'user.email',
            'user.hashed_password',
            'user.is_active',
            'user.confirmation'
        )


class BaseProfile(BaseModel):
    first_name: str
    last_name: str

class CreateProfile(BaseProfile):
    user_id: str


class UpdateProfile(BaseProfile):
    pass


class ProfileAddCity(BaseModel):
    cities: list[int]


class ProfileMe(BaseProfile):
    cities: CreateCity

Tortoise.init_models(settings.MODELS, 'models')

Profile_Pydantic = pydantic_model_creator(
    Profile,
    name='Profile'
)
ProfileIn_Pydantic = pydantic_model_creator(
    Profile,
    name='Profile',
    exclude_readonly=True
)
