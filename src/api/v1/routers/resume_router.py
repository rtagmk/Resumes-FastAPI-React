"""
This module defines the API endpoints for resume management.

It includes routes for creating, reading, updating, and deleting resumes.
It utilizes FastAPI's routing and dependency injection features, along
with SQLAlchemy for database interactions and authentication for
securing the endpoints.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from .... import schemas
from ....dao import ResumeDAO
from ....security import get_current_user
from ....services import ai_service

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new resume",
    description="Creates a new resume in the system. Requires authentication.",
)
async def create_resume(
    resume: schemas.ResumeCreate,
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.Resume:
    """
    Create a new resume.

    Args:
        resume (schemas.ResumeCreate): The resume to create.
        current_user (schemas.User): The current user.

    Returns:
        schemas.Resume: The created resume.
    """
    logger.info("Received request to create a resume.")

    data = resume.model_dump()
    data["owner_id"] = current_user.id

    new_db_resume = await ResumeDAO.create_record(data)

    return schemas.Resume.model_validate(new_db_resume)


@router.get(
    "/{resume_id}",
    summary="Get resume by ID",
    description="Retrieves a specific resume by its ID. "
    "Requires authentication.",
)
async def read_resume(
    resume_id: int,
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.Resume:
    """
    Get resume by ID.

    Args:
        resume_id (int): The ID of the resume to retrieve.
        current_user (schemas.User): The current user.

    Returns:
        schemas.Resume: The retrieved resume.

    Raises:
        HTTPException: If the resume is not found or the user does not have
        sufficient permissions.
    """
    logger.info("Received request to get a resume by id.")

    filter_by = {"id": resume_id, "owner_id": current_user.id}
    resume = await ResumeDAO.get_records_or_record(
        return_one=True, **filter_by
    )
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    return schemas.Resume.model_validate(resume)


@router.get(
    "/",
    summary="Get all user's resumes",
    description="Retrieves a list of user's resumes. "
    "Supports pagination with skip and limit parameters. "
    "Requires authentication.",
)
async def read_resumes(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user),
) -> List[schemas.Resume]:
    """
    Get all resumes.

    Args:
        skip (int, optional): The number of resumes to skip. Defaults to 0.
        limit (int, optional): The maximum number of resumes to return.
                                Defaults to 100.
        current_user (schemas.User): The current user.

    Returns:
        List[schemas.Resume]: A list of resumes.
    """
    logger.info("Received request to get all resumes of user.")

    filter_by = {"owner_id": current_user.id}
    resumes = await ResumeDAO.get_records_or_record(
        return_one=False, skip=skip, limit=limit, **filter_by
    )
    if resumes is None:
        return []

    if isinstance(resumes, list):
        return [schemas.Resume.model_validate(resume) for resume in resumes]
    return [schemas.Resume.model_validate(resumes)]


@router.put(
    "/{resume_id}",
    summary="Update resume",
    description="Updates an existing resume by its ID. "
    "Requires authentication to modify the resume.",
)
async def update_resume(
    resume_id: int,
    resume: schemas.ResumeUpdate,
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.Resume:
    """
    Update resume.

    Args:
        resume_id (int): The ID of the resume to update.
        title (str): The title for update.
        content (str): The content for update.
        current_user (schemas.User): The current user.

    Returns:
        schemas.Resume: The updated resume.

    Raises:
        HTTPException: If the resume is not found or the user does not have
        sufficient permissions.
    """
    logger.info("Received request to update a resume.")

    def valid_value(key_value):
        _, value = key_value
        return (
            isinstance(value, str) and not value.isspace() and len(value) > 0
        )

    update_data = resume.model_dump()
    update_data = dict(filter(valid_value, update_data.items()))

    if len(update_data) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No data to update",
        )

    updated_resume = await ResumeDAO.update_record(
        obj_id=resume_id, obj_data=update_data, owner_id=current_user.id
    )
    if updated_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    return schemas.Resume.model_validate(updated_resume)


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete resume",
    description="Deletes a resume by its ID. "
    "Requires authentication to delete the resume.",
)
async def delete_resume(
    resume_id: int,
    current_user: schemas.User = Depends(get_current_user),
) -> None:
    """
    Delete resume.

    Args:
        resume_id (int): The ID of the resume to delete.
        current_user (schemas.User): The current user.

    Returns:
        dict: A dictionary with the key "ok" and value True.

    Raises:
        HTTPException: If the resume is not found or the user does not have
        sufficient permissions.
    """
    logger.info("Received request to delete a resume.")

    resume = await ResumeDAO.delete_record(
        obj_id=resume_id, owner_id=current_user.id
    )
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")


@router.post("/resume/{resume_id}/improve", tags=["AI"])
async def improve_resume(
    resume_id: int,
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.Resume:
    """
    Improve resume content.

    Args:
        resume_id (int): The ID of the resume to improve.
        current_user (schemas.User): The current user.

    Returns:
        schemas.Resume: The improved resume.

    Raises:
        HTTPException: If the resume or content are not found
        or the user does not have sufficient permissions.
    """
    logger.info("Received request to improve a resume's content.")

    filter_by = {"id": resume_id, "owner_id": current_user.id}
    resume = await ResumeDAO.get_records_or_record(
        return_one=True, **filter_by
    )
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")

    original_content = resume.content  # type: ignore
    if original_content is None:
        raise HTTPException(status_code=404, detail="Content not found")

    ai_result_text = await ai_service.improve_resume_content(
        original_content=original_content
    )

    data_update = {
        "content": ai_result_text,
        "original_content": original_content,
    }

    resume = await ResumeDAO.update_record(
        obj_id=resume_id,
        obj_data=data_update,
        owner_id=current_user.id,
        use_history=True,
    )

    return schemas.Resume.model_validate(resume)
