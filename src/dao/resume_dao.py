"""
Resume Data Access Object (DAO) module for interacting with resume data in the
database.
"""

from typing import Optional

from loguru import logger
from sqlalchemy import delete, insert, update

from ..database import async_session
from ..models import DBResume, DBResumeHistory
from .base_dao import BaseDAO


class ResumeDAO(BaseDAO[DBResume]):
    """
    Base Data Access Object (DAO) for interacting with resume data in the
    database.
    """

    model = DBResume

    @classmethod
    async def update_record(
        cls,
        obj_id: int,
        obj_data: dict[str, str],
        owner_id: Optional[int] = None,
        use_history: bool = False,
    ) -> DBResume | None:
        """
        Update an existing resume in the database.

        Args:
            obj_id (int): The ID of the record to update.
            obj_data (dict): The data for updating the record.
            owner_id (int): The ID of the record's owner to update.
            use_history (bool): Add record to history table.

        Returns:
            The updated record or None if not found.
        """
        logger.debug("Starting update record for model {model.__name__}")

        async with async_session() as session:
            if (
                use_history
                and "content" in obj_data
                and "original_content" in obj_data
            ):
                logger.debug(
                    "Starting log improved content "
                    "for model {DBResumeHistory.__name__}"
                )
                improved_content_to_log = obj_data.get("content")
                original_content_for_log = obj_data.get("original_content")

                history_query = insert(DBResumeHistory).values(
                    resume_id=obj_id,
                    original_content=original_content_for_log,
                    improved_content=improved_content_to_log,
                )
                await session.execute(history_query)
                del obj_data["original_content"]

            query = (
                update(cls.model)
                .where(cls.model.id == obj_id)
                .where(cls.model.owner_id == owner_id)
                .values(**obj_data)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete_record(
        cls, obj_id: int, owner_id: Optional[int] = None
    ) -> int | None:
        """
        Delete a record from the database.

        Args:
            obj_id (int): The ID of the record to delete.
        """
        logger.debug("Starting delete record for model {model.__name__}")

        async with async_session() as session:
            query = (
                delete(cls.model)
                .where(cls.model.id == obj_id)
                .where(cls.model.owner_id == owner_id)
                .returning(cls.model.id)
            )
            result = await session.execute(query)
            deleted_id = result.scalar_one_or_none()
            await session.commit()
            return deleted_id
