"""
Main module with settings for testing
"""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings


@pytest_asyncio.fixture(scope="session")
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session for each test.
    """
    engine = create_async_engine(settings.database_url_async)
    async_session = async_sessionmaker(
        engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    )

    async with async_session() as session:
        yield session


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates and yields an asyncio event loop for the test session.

    This fixture ensures that a new event loop is created for each test session,
    preventing interference between tests that rely on asyncio.  The loop is
    closed after the session completes.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
