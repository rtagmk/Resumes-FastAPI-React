"""
API endpoints for the application.
"""

from .resume_router import router as resume_router
from .user_router import router as user_router

__all__ = ["resume_router", "user_router"]
