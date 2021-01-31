from jose import jwt

from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends
)
from fastapi.security import OAuth2PasswordRequestForm

from services.auth import Auth

from config.settings import Settings

from models import users
from models.auth import LoginModel

settings = Settings()
auth_router = APIRouter()

@auth_router.post('/register')
async def register(form_data: users.CreateUser):
    if await users.UserModel.get_or_none(email=form_data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with this email already exists'
        )
    user = await users.UserModel.create(
        email=form_data.email,
        hashed_password=Auth.get_password_hash(
            form_data.password
        )
    )
    confirmation = Auth.get_confirmation_token(user.id)
    user.confirmation = confirmation['jti']
    print(confirmation['token'])
    await user.save()
    return await users.User_Pydantic.from_tortoise_orm(user)


@auth_router.get('/verify/{token}')
async def verify(token: str):
    # pylint:disable=(raise-missing-from)
    invalid_token_error = HTTPException(status_code=400, detail='Invalid token')
    print(token)
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.TOKEN_ALGORITHM
        )
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail='Token has expired')

    if payload['scope'] != 'registration':
        raise invalid_token_error

    user = await users.UserModel.get_or_none(id=payload['sub'])

    if not user or str(user.confirmation) != payload['jti']:
        raise invalid_token_error

    if user.is_active:
        raise HTTPException(status_code=403, detail='User already activated')

    user.confirmation = None
    user.is_active = True
    await user.save()
    return await users.User_Pydantic.from_tortoise_orm(user)


@auth_router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await Auth.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    user_obj = await users.User_Pydantic.from_tortoise_orm(user)
    to_encode = user_obj.dict()
    to_encode['id'] = str(to_encode.get('id'))
    token = Auth.get_token(to_encode, settings.REGISTRATION_TOKEN_LIFETIME)

    return {'access_token' : token, 'token_type' : 'bearer'}


# @auth_router.post('/login')
# async def login(auth_data: LoginModel):
#     user = await Auth.authenticate_user(
#         auth_data.email,
#         auth_data.password
#     )
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail='Invalid username or password'
#         )
#     user_obj = await users.User_Pydantic.from_tortoise_orm(user)
#     to_encode = user_obj.dict()
#     to_encode['id'] = str(to_encode.get('id'))
#     token = Auth.get_token(to_encode, settings.REGISTRATION_TOKEN_LIFETIME)
#     return {'access_token' : token, 'token_type' : 'bearer'}
