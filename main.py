"""NIW Tools API — shared backend for all NIW petition tool pages."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.db import close_db
from modules.downloads.router import router as downloads_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    yield
    await close_db()


app = FastAPI(
    title="NIW Tools API",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url=None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok", "version": "1.0.0"}


app.include_router(downloads_router, prefix="/api/v1/downloads", tags=["Downloads"])
