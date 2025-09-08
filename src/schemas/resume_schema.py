"""
Pydantic schemas for resume data.
"""

from typing import Optional

from pydantic import BaseModel, Field

class ResumeBase(BaseModel):
    """
    Base schema for resume.
    """

    title: str = Field(
        ...,
        title="Resume title",
        description="The title of the resume. Must be non empty.",
        min_length=1,
    )
    content: Optional[str] = Field(
        None,
        title="Resume content.",
        description="A detailed description of the resume.",
    )


class ResumeCreate(ResumeBase):
    """
    Schema for creating a new Resume.
    """

    model_config = {
        "title": "Resume creation data",
        "json_schema_extra": {
            "description": "Schema for creating a new Resume."
        },
    }


class ResumeUpdate(ResumeBase):
    """
    Schema for updating an existing Resume.
    """

    title: Optional[str] = Field(
        None,
        title="Resume title",
        description="The title of the Resume. Must be non empty.",
    )

    model_config = {
        "title": "Resume update data",
        "json_schema_extra": {
            "description": "Schema for updating an existing Resume."
        },
    }


class Resume(ResumeBase):
    """
    Schema for representing a Resume.
    """

    id: int = Field(
        ...,
        title="Resume ID",
        description="The ID of the Resume.",
    )

    model_config = {
        "title": "Resume data",
        "json_schema_extra": {"description": "Schema of Resume data."},
        "from_attributes": True,
    }
