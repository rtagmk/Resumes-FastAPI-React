"""
Pydantic schemas for User data.
"""

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base schema for User, containing common attributes.
    """

    username: str = Field(
        ...,
        title="User name",
        description="The name of the user. Must be non empty.",
        min_length=1,
    )
    email: EmailStr = Field(
        ...,
        title="User email",
        description="The email of the user.",
    )


class UserCreate(UserBase):
    """
    Schema for creating a new User.
    """

    password: str = Field(
        ...,
        title="User password",
        description="The password of the user.",
        min_length=8,
    )

    model_config = {
        "title": "User creation data",
        "json_schema_extra": {
            "description": "Schema for creating a new user."
        },
    }


class UserUpdate(BaseModel):
    """
    Schema for updating an existing User.
    """

    username: str = Field(
        "",
        title="User name",
        description="The name of the user. Must be non empty.",
        min_length=1,
    )
    email: EmailStr = Field(
        "",
        title="User email",
        description="The email of the user.",
    )

    model_config = {
        "title": "User update data",
        "json_schema_extra": {
            "description": "Schema for updating an existing user."
        },
    }


class User(UserBase):
    """
    Schema for representing a User.
    """

    id: int = Field(
        ...,
        title="User ID",
        description="The ID of the user.",
    )

    model_config = {
        "title": "User data",
        "json_schema_extra": {"description": "Schema of user data."},
        "from_attributes": True,
    }


class Token(BaseModel):
    """
    Schema for representing a JWT token.
    """

    access_token: str = Field(
        ...,
        title="Access token",
        description="The JWT access token.",
    )
    token_type: str = Field(
        "bearer",
        title="Token type",
        description="The type of the token.",
    )

    model_config = {
        "title": "JWT token data",
        "json_schema_extra": {"description": "Schema for JWT token data."},
    }


class TokenData(BaseModel):
    """
    Schema for representing the data within a JWT token.
    """

    userid: str | None = Field(
        None,
        title="User ID",
        description="The userid within the JWT token.",
    )
