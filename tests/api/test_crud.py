"""
Module for testing crud
"""

import bcrypt
import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import UserDAO
from src.dao import ResumeDAO
from src.models import DBResume, DBUser
from src.security import hash_password


async def create_user_in_db(
    get_db: AsyncSession,
    username: str,
    email: str,
) -> DBUser | None:
    """
    Creates a new user in the database.
    Returns the created user object, or None if creation fails.
    """
    try:
        result = await get_db.execute(
            text(
                "INSERT INTO users (username, email, hashed_password) "
                "VALUES (:username, :email, :hashed_password) "
                "RETURNING id, username, email, hashed_password"
            ),
            {
                "username": username,
                "email": email,
                "hashed_password": hash_password("password"),
            },
        )
        await get_db.commit()

        row = result.first()
        if row:
            return DBUser(
                id=row[0],
                username=row[1],
                email=row[2],
                hashed_password=row[3],
            )
        return None
    except SQLAlchemyError:
        await get_db.rollback()
        return None


async def delete_test_user_form_db(
    get_db: AsyncSession, test_username: str
) -> None:
    """
    Delete test user from database if exists.
    """

    result = await get_db.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": test_username},
    )
    user_exists = bool(result.scalar_one_or_none())

    if user_exists:
        await get_db.execute(
            text("DELETE FROM users WHERE username = :username").params(
                username=test_username
            )
        )
        await get_db.commit()


async def get_user_from_db(
    get_db: AsyncSession, test_username: str
) -> DBUser | None:
    """
    Retrieves a user from the database by username.
    """

    result = await get_db.execute(
        text(
            "SELECT id, username, email, hashed_password "
            "FROM users WHERE username = :username"
        ),
        {"username": test_username},
    )
    row = result.first()
    if row:
        return DBUser(
            id=row[0], username=row[1], email=row[2], hashed_password=row[3]
        )
    return None


async def create_resume_in_db(
    get_db: AsyncSession,
    title: str,
    content: str | None,
    owner_id: int,
    
) -> DBResume | None:
    """
    Creates a new resume in the database.
    Returns the created resume object, or None if creation fails.
    """
    try:
        result = await get_db.execute(
            text(
                "INSERT INTO resumes (title, content, owner_id) "
                "VALUES (:title, :content, :owner_id) "
                "RETURNING id, title, content, owner_id"
            ),
            {
                "title": title,
                "content": content,
                "owner_id": owner_id,
            },
        )
        await get_db.commit()

        row = result.first()
        if row:
            return DBResume(
                id=row[0],
                title=row[1],
                content=row[2],
                owner_id=row[3],
                
            )
        return None

    except SQLAlchemyError as e:
        await get_db.rollback()
        print(f"Error creating resume: {e}")
        return None


async def get_resume_from_db(
    get_db: AsyncSession,
    resume_id: int,
) -> DBResume | None:
    """
    Retrieves a resume from the database by title.
    """

    result = await get_db.execute(
        text(
            "SELECT id, title, content, owner_id "
            "FROM resumes WHERE id = :id"
        ),
        {"id": resume_id},
    )
    row = result.first()
    if row:
        return DBResume(
            id=row[0],
            title=row[1],
            content=row[2],
            owner_id=row[3],
        )
    return None


@pytest.mark.asyncio
async def test_get_hash_password():
    """
    Test getting a hash_password.
    """
    password = "password123"
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert bcrypt.checkpw(
        password.encode("utf-8"), hashed_password.encode("utf-8")
    )


@pytest.mark.asyncio
async def test_create_user(get_db: AsyncSession):
    """
    Test creating a user.
    """
    test_username = "testuser"
    test_email = "test@example.com"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)

    data = {
        "username": test_username,
        "email": test_email,
        "hashed_password": hash_password("password123"),
    }

    user = await UserDAO.create_record(obj_data=data)
    assert user is not None

    retrieved_user = await get_user_from_db(
        get_db=get_db, test_username=test_username
    )
    assert retrieved_user is not None
    assert retrieved_user.username == test_username
    assert retrieved_user.email == test_email


@pytest.mark.asyncio
async def test_get_user(get_db: AsyncSession):
    """
    Test getting a user by ID.
    """
    test_username = "testuser"
    test_email = "test@example.com"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)
    user = await create_user_in_db(
        get_db=get_db, username=test_username, email=test_email
    )
    assert user is not None

    retrieved_user = await UserDAO.get_records_or_record(
        return_one=True, id=user.id
    )
    assert retrieved_user is not None
    assert isinstance(retrieved_user, DBUser)
    assert retrieved_user.username == test_username
    assert retrieved_user.email == test_email


@pytest.mark.asyncio
async def test_get_user_by_username(get_db: AsyncSession):
    """
    Test getting a user by username.
    """
    test_username = "testuser"
    test_email = "test@example.com"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)
    user = await create_user_in_db(
        get_db=get_db, username=test_username, email=test_email
    )
    assert user is not None

    retrieved_user = await UserDAO.get_records_or_record(
        return_one=True, username=test_username
    )
    assert retrieved_user is not None
    assert isinstance(retrieved_user, DBUser)
    assert retrieved_user.username == test_username
    assert retrieved_user.email == test_email


@pytest.mark.asyncio
async def test_get_users(get_db: AsyncSession):
    """
    Test getting users.
    """
    test_username1 = "testuser1"
    test_email1 = "test1@example.com"
    test_username2 = "testuser2"
    test_email2 = "test2@example.com"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username1)
    await delete_test_user_form_db(get_db=get_db, test_username=test_username2)
    user1 = await create_user_in_db(
        get_db=get_db, username=test_username1, email=test_email1
    )
    assert user1 is not None

    user2 = await create_user_in_db(
        get_db=get_db, username=test_username2, email=test_email2
    )
    assert user2 is not None

    users = await UserDAO.get_records_or_record()
    assert users is not None
    assert isinstance(users, list)
    assert any(user.username == test_username1 for user in users)
    assert any(user.username == test_username2 for user in users)


@pytest.mark.asyncio
async def test_update_user(get_db: AsyncSession):
    """
    Test updating a user.
    """
    test_username = "testuser"
    test_email = "test@example.com"
    updated_username = "newuser"
    updated_email = "new@example.com"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)
    await delete_test_user_form_db(
        get_db=get_db, test_username=updated_username
    )
    user = await create_user_in_db(
        get_db=get_db, username=test_username, email=test_email
    )
    assert user is not None

    user_update = {"username": updated_username, "email": updated_email}

    updated_user = await UserDAO.update_record(
        obj_id=user.id, obj_data=user_update
    )
    assert updated_user is not None
    assert updated_user.username == updated_username
    assert updated_user.email == updated_email

    retrieved_user = await get_user_from_db(get_db, updated_username)
    assert retrieved_user is not None
    assert retrieved_user.username == updated_username
    assert retrieved_user.email == updated_email


@pytest.mark.asyncio
async def test_delete_user(get_db: AsyncSession):
    """
    Test deleting a user.
    """
    test_username = "testuser"
    test_email = "test@example.com"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)
    user = await create_user_in_db(
        get_db=get_db, username=test_username, email=test_email
    )
    assert user is not None

    await UserDAO.delete_record(obj_id=user.id)
    retrieved_user = await get_user_from_db(get_db, test_username)
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_create_resume(get_db: AsyncSession):
    """
    Test creating a resume.
    """
    test_username = "testuser"
    test_email = "test@example.com"
    test_resume_title = "testresume"
    test_resume_content = "testcontent"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)
    user = await create_user_in_db(
        get_db=get_db, username=test_username, email=test_email
    )
    assert user is not None

    resume_create = {
        "title": test_resume_title,
        "content": test_resume_content,
        "owner_id": user.id,
    }

    resume = await ResumeDAO.create_record(obj_data=resume_create)
    assert resume is not None

    retrieved_resume = await get_resume_from_db(get_db, resume.id)
    assert retrieved_resume is not None
    assert retrieved_resume.title == test_resume_title
    assert retrieved_resume.content == test_resume_content


@pytest.mark.asyncio
async def test_get_resume(get_db: AsyncSession):
    """
    Test getting a resume.
    """
    test_username = "testuser"
    test_email = "test@example.com"
    test_resume_title = "testresume"
    test_resume_content = "testcontent"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)
    user = await create_user_in_db(
        get_db=get_db, username=test_username, email=test_email
    )
    assert user is not None

    resume = await create_resume_in_db(
        get_db=get_db,
        title=test_resume_title,
        content=test_resume_content,
        owner_id=user.id,
    )
    assert resume is not None

    retrieved_resume = await ResumeDAO.get_records_or_record(
        return_one=True, id=resume.id
    )
    assert retrieved_resume is not None
    assert isinstance(retrieved_resume, DBResume)
    assert retrieved_resume.title == test_resume_title
    assert retrieved_resume.content == test_resume_content


@pytest.mark.asyncio
async def test_get_resumes(get_db: AsyncSession):
    """
    Test getting resumes.
    """
    test_username = "testuser"
    test_email = "test@example.com"
    test_resume_title1 = "testresume1"
    test_resume_content1 = "testcontent1"
    test_resume_title2 = "testresume2"
    test_resume_content2 = "testcontent2"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)
    user = await create_user_in_db(
        get_db=get_db, username=test_username, email=test_email
    )
    assert user is not None

    resume1 = await create_resume_in_db(
        get_db=get_db,
        title=test_resume_title1,
        content=test_resume_content1,
        owner_id=user.id,
    )
    assert resume1 is not None

    resume2 = await create_resume_in_db(
        get_db=get_db,
        title=test_resume_title2,
        content=test_resume_content2,
        owner_id=user.id,
    )
    assert resume2 is not None

    resumes = await ResumeDAO.get_records_or_record(owner_id=user.id)
    assert resumes is not None
    assert isinstance(resumes, list)
    assert any(resume.title == test_resume_title1 for resume in resumes)
    assert any(resume.title == test_resume_title2 for resume in resumes)


@pytest.mark.asyncio
async def test_update_resume(get_db: AsyncSession):
    """
    Test updating a resume.
    """
    test_username = "testuser"
    test_email = "test@example.com"
    test_resume_title = "testresume"
    test_resume_content = "testcontent"
    updated_resume_title = "newtitle"
    updated_resume_content = "newcontent"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)
    user = await create_user_in_db(
        get_db=get_db, username=test_username, email=test_email
    )
    assert user is not None

    resume = await create_resume_in_db(
        get_db=get_db,
        title=test_resume_title,
        content=test_resume_content,
        owner_id=user.id,
    )
    assert resume is not None

    resume_update = {
        "title": updated_resume_title,
        "content": updated_resume_content,
    }

    updated_resume = await ResumeDAO.update_record(
        obj_id=resume.id, obj_data=resume_update, owner_id=user.id
    )
    assert updated_resume is not None
    assert updated_resume.title == updated_resume_title
    assert updated_resume.content == updated_resume_content

    retrieved_resume = await get_resume_from_db(get_db, updated_resume.id)
    assert retrieved_resume is not None
    assert retrieved_resume.title == updated_resume_title
    assert retrieved_resume.content == updated_resume_content


@pytest.mark.asyncio
async def test_delete_resume(get_db: AsyncSession):
    """
    Test deleting a resume.
    """
    test_username = "testuser"
    test_email = "test@example.com"
    test_resume_title = "testresume"
    test_resume_content = "testcontent"

    await delete_test_user_form_db(get_db=get_db, test_username=test_username)
    user = await create_user_in_db(
        get_db=get_db, username=test_username, email=test_email
    )
    assert user is not None

    resume = await create_resume_in_db(
        get_db=get_db,
        title=test_resume_title,
        content=test_resume_content,
        owner_id=user.id,
    )
    assert resume is not None

    deleted_id = await ResumeDAO.delete_record(obj_id=resume.id, owner_id=user.id)
    assert deleted_id is not None
    assert deleted_id == resume.id
    retrieved_resume = await get_resume_from_db(get_db, resume.id)
    assert retrieved_resume is None
