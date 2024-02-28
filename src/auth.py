from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException
from passlib.context import CryptContext
from .local_database import user_database
from .schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_route = APIRouter()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def fake_decoded_token(token: str):
    user = next(filter(lambda user: user["email"] == token, user_database), None)
    if user:
        return user


def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decoded_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(**user)


@auth_route.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = next(
        filter(lambda user: user["email"] == form_data.username, user_database), None
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    if not verify_password(form_data.password, user.get("hashed_password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provided not correct password",
        )

    return {"access_token": user.get("email"), "type": "bearer"}
