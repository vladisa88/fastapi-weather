from passlib.hash import bcrypt

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from pydantic import BaseModel, EmailStr


class UserModel(models.Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(null=False, max_length=255)
    hashed_password = fields.CharField(null=True, max_length=255)
    is_active = fields.BooleanField(null=False, default=False)
    confirmation = fields.UUIDField(null=True)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)

    class Meta:
        table: str = 'users'


class CreateUser(BaseModel):
    email: EmailStr
    password: str


User_Pydantic = pydantic_model_creator(
    UserModel,
    name='User',
    exclude=('hashed_password', 'confirmation')
)
