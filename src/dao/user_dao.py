"""
User Data Access Object (DAO) module for interacting with user data in the
database.
"""

from loguru import logger
from sqlalchemy import or_, select

from ..database import async_session
from ..models import Base, DBUser
from .base_dao import BaseDAO


class UserDAO(BaseDAO[DBUser]):
    """
    Base Data Access Object (DAO) for interacting with user data in the
    database.
    """

    model = DBUser

    @classmethod
    async def create_record(
        cls, obj_data: dict[str, str]
    ) -> Base | DBUser | None:
        """
        Create a new record in the database.

        Args:
            obj_data (dict): The data for creating a new record.

        Returns:
            The created record or None if user exist.
        """
        logger.debug("Starting create record for model {model.__name__}")

        async with async_session() as session:
            query = select(cls.model).filter(
                or_(
                    DBUser.username == obj_data.get("username"),
                    DBUser.email == obj_data.get("email"),
                )
            )
            result = await session.execute(query)

            exist_user = result.scalar_one_or_none()
            if exist_user:
                return None

        return await super(UserDAO, cls).create_record(obj_data)
