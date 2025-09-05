"""
Base Data Access Object (DAO) module for interacting with the database.

This module provides a base class and methods to perform CRUD operations
on specific models.
"""

from typing import Any, Generic, List, Optional, TypeVar

from loguru import logger
from sqlalchemy import delete, insert, select, update

from ..database import async_session
from ..models import Base

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    """
    Base Data Access Object (DAO) for interacting with the database.

    This class provides a set of methods to perform CRUD operations on the
    specified model.

    Attributes:
        model (Any): The SQLAlchemy model that this DAO is associated with.
    """

    model: Any = None

    @classmethod
    async def get_records_or_record(
        cls,
        return_one: bool = False,
        skip: int = 0,
        limit: int = 100,
        **filter_by,
    ) -> Optional[T | List[T]]:
        """
        Retrieve a single record or all records from the database
        based on the provided filters.

        Args:
            return_one (bool): If True, returns a single record; otherwise,
                                returns all records.
            filter_by (dict): The filter conditions to apply to the query.

        Returns:
            The retrieved record(s) as a single object if `return_one` is True,
            or as a list of objects if `return_one` is False.
        """
        logger.debug(
            "Starting get records or record for model {model.__name__}"
        )

        async with async_session() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .offset(skip)
                .limit(limit)
            )
            result = await session.execute(query)

            if return_one:
                return result.scalar_one_or_none()
            return list(result.scalars().all())

    @classmethod
    async def create_record(cls, obj_data: dict[str, Any]) -> T:
        """
        Create a new record in the database.

        Args:
            obj_data (dict): The data for creating a new record.

        Returns:
            The created record.
        """
        logger.debug(
            "Starting create record for model {model.__name__}"
        )

        async with async_session() as session:
            query = insert(cls.model).values(**obj_data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def update_record(
        cls, obj_id: int, obj_data: dict[str, Any]
    ) -> Optional[T]:
        """
        Update an existing record in the database.

        Args:
            obj_id (int): The ID of the record to update.
            obj_data (dict): The data for updating the record.

        Returns:
            The updated record or None if not found.
        """
        logger.debug(
            "Starting update record for model {model.__name__}"
        )

        async with async_session() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == obj_id)
                .values(**obj_data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete_record(cls, obj_id: int) -> int | None:
        """
        Delete a record from the database.

        Args:
            obj_id (int): The ID of the record to delete.
        """
        logger.debug(
            "Starting delete record for model {model.__name__}"
        )

        async with async_session() as session:
            query = (
                delete(cls.model)
                .where(cls.model.id == obj_id)
                .returning(cls.model.id)
            )
            result = await session.execute(query)
            deleted_id = result.scalar_one_or_none()
            await session.commit()
            return deleted_id
