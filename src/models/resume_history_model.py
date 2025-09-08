"""
SQLAlchemy models for Resume's history data.
"""

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import Base


class DBResumeHistory(Base):
    """
    Resume's history model.
    """

    __tablename__ = "resume_history"

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False
    )
    original_content: Mapped[str] = mapped_column(Text, nullable=False)
    improved_content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
