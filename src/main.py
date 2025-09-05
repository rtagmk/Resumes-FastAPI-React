"""
This module defines the main FastAPI application.

It configures and includes routers for different API endpoints,
such as users and resume. It also sets up the application's title
based on the settings defined in the `config` module.
"""

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from .api.v1.routers import resume_router, user_router

logger.remove()

logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
    "| <level>{level: <8}</level> "
    "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>",
    level="INFO",
)

logs_dir = Path("logs")
logs_dir.mkdir(parents=True, exist_ok=True)

log_file_path = logs_dir / "app.log"

logger.add(
    log_file_path,
    rotation="10 MB",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
    enqueue=True,
)

PROJECT_NAME = "Resume app"
app = FastAPI(title=PROJECT_NAME, redirect_slashes=False)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/v1/users", tags=["users"])
app.include_router(resume_router, prefix="/v1/resumes", tags=["resumes"])


app.mount("/", StaticFiles(directory="static", html=True), name="static")
