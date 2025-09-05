"""
SQLAlchemy models for User data.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class DBUser(Base):
    """
    User model.
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
