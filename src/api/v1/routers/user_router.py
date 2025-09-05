"""
This module defines the API endpoints for user management.

It includes routes for creating, reading, updating, and deleting users.
It utilizes FastAPI's routing and dependency injection features, along
with SQLAlchemy for database interactions.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from .... import schemas
from ....dao import UserDAO
from ....models import DBUser
from ....security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Registers a new user in the system. "
    "Requires a unique username and email.",
)
async def create_user(user: schemas.UserCreate) -> schemas.User:
    """
    Create a new user.

    Args:
        user (schemas.UserCreate): The user to create.

    Returns:
        schemas.User: The created user.

    Raises:
        HTTPException: If the username or email already exists.
    """
    logger.info("Received request to register new user.")

    data = user.model_dump()
    data["hashed_password"] = hash_password(user.password)
    del data["password"]
    new_db_user = await UserDAO.create_record(data)
    if not new_db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    return schemas.User.model_validate(new_db_user)


@router.get(
    "/{user_id}",
    summary="Get user by ID",
    description="Retrieves a specific user by ID.",
)
async def read_user(user_id: int) -> schemas.User:
    """
    Get user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        schemas.User: The retrieved user.

    Raises:
        HTTPException: If the user is not found.
    """
    logger.info("Received request to get a user by id.")

    exist_user = await UserDAO.get_records_or_record(
        return_one=True, id=user_id
    )
    if exist_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return schemas.User.model_validate(exist_user)


@router.get(
    "/",
    summary="Get all users",
    description="Retrieves a list of all users. "
    "Supports pagination with skip and limit parameters.",
)
async def read_users(
    skip: int = 0,
    limit: int = 100,
) -> List[schemas.User]:
    """
    Get all users.

    Args:
        skip (int, optional): The number of users to skip. Defaults to 0.
        limit (int, optional): The maximum number of users to return.
                                Defaults to 100.

    Returns:
        List[schemas.User]: A list of users.
    """
    logger.info("Received request to get all users.")

    users = await UserDAO.get_records_or_record(skip=skip, limit=limit)
    if not users:
        return []
    if isinstance(users, list):
        return [schemas.User.model_validate(user) for user in users]
    return [schemas.User.model_validate(users)]


@router.put(
    "/{user_id}",
    summary="Update user information",
    description="Updates an existing user by ID.",
)
async def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    """
    Update user.

    Args:
        user_id (int): The ID of the user to update.
        user (schemas.UserUpdate): The updated user data.

    Returns:
        schemas.User: The updated user.

    Raises:
        HTTPException: If the user is not found or the user does not have
        sufficient permissions.
    """
    logger.info("Received request to update a user.")

    def valid_value(key_value):
        _, value = key_value
        return (
            isinstance(value, str) and not value.isspace() and len(value) > 0
        )

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    update_data = user.model_dump()
    update_data = dict(filter(valid_value, update_data.items()))

    if len(update_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No data to update",
        )

    updated_user = await UserDAO.update_record(
        obj_id=user_id, obj_data=update_data
    )
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return schemas.User.model_validate(updated_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Deletes a user by ID.",
)
async def delete_user(
    user_id: int, current_user: schemas.User = Depends(get_current_user)
) -> None:
    """
    Delete user.

    Args:
        user_id (int): The ID of the user to delete.

    Raises:
        HTTPException: If the user is not found or the user does not have
        sufficient permissions.
    """
    logger.info("Received request to delete a user.")

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    deleted_id = await UserDAO.delete_record(obj_id=user_id)
    if deleted_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post(
    "/login",
    summary="Generate access token",
    description="Generates an access token for authenticated users. "
    "Requires a valid username and password.",
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.Token:
    """
    Endpoint for generating access tokens.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing
                                                the username and password.

    Returns:
        schemas.Token: The generated access token.

    Raises:
        HTTPException: If the username or password is incorrect.
    """
    logger.info(
        f"Received request to get token for user {form_data.username}."
    )

    db_user = await UserDAO.get_records_or_record(
        True, username=form_data.username
    )
    if not isinstance(db_user, DBUser) or not verify_password(
        plain_password=form_data.password,
        hashed_password=db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=db_user.id)
    return schemas.Token(access_token=access_token, token_type="bearer")
