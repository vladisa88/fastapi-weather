import uuid
from datetime import datetime, timedelta

from jose import jwt
from passlib.hash import bcrypt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import UUID4

from config.settings import get_settings
from models.users import UserModel, User_Pydantic

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/token')

class Auth:

    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def get_token(data: dict, expires_delta: int):
        to_encode = data.copy()
        to_encode.update({
            'exp': datetime.now() + timedelta(seconds=expires_delta),
            'iss': settings.APP_NAME
        })
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.TOKEN_ALGORITHM
        )

    @staticmethod
    def get_confirmation_token(user_id: UUID4) -> dict:
        jti = uuid.uuid4()
        claims = {
            'sub': str(user_id),
            'scope': 'registration',
            'jti': str(jti)
        }
        return {
            'jti': jti,
            'token': Auth.get_token(
                claims,
                settings.REGISTRATION_TOKEN_LIFETIME
            )
        }

    @staticmethod
    async def authenticate_user(email: str, password: str) -> UserModel or False:
        user = await UserModel.get(email=email)

        if not user:
            return False

        if not user.verify_password(password):
            return False

        return user

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
        try:
            payload = jwt.decode(
                token=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.TOKEN_ALGORITHM]
            )
            user = await UserModel.get(id=payload.get('id'))
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Invalid username or password'
            )
        
        return await User_Pydantic.from_tortoise_orm(user)
