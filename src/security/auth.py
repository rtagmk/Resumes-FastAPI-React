"""
Authentication and authorization utilities using JWT.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from ..config import settings
from ..dao import UserDAO
from ..schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.

    Args:
        subject (str | Any): The subject of the token.
        expires_delta (timedelta | None): The expiration delta of the token.
            Defaults to None.

    Returns:
        str: The encoded JWT access token.
    """

    expires_at = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.access_token_expire_minutes)
    )

    to_encode = {"exp": expires_at, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user from the JWT token.

    Args:
        token (str, optional): The JWT token.

    Returns:
        User: The current user object.

    Raises:
        HTTPException: If the credentials could not be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        str_userid = payload.get("sub")
        if str_userid is None or not str_userid.isnumeric():
            raise credentials_exception
        
        userid = int(str_userid)

        user = await UserDAO.get_records_or_record(
            return_one=True, id=userid
        )
        if user is None:
            raise credentials_exception

        return User.model_validate(user)

    except JWTError as e:
        raise credentials_exception from e
