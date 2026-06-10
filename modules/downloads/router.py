"""NIW Tools API — Download tracking.
Records tool_id, IP address, and user-agent for every download event.
Endpoints are public — download counts are public-facing metrics.
"""
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db

router = APIRouter()


def _get_client_ip(request: Request) -> str:
    # Railway sits behind a proxy — real IP is in X-Forwarded-For
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()[:45]
    return (request.client.host or "")[:45]


class DownloadCountResponse(BaseModel):
    tool_id: str
    count: int


class DownloadRecordResponse(BaseModel):
    tool_id: str
    count: int
    recorded: bool


@router.post("/{tool_id}", response_model=DownloadRecordResponse)
async def record_download(
    tool_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    ip = _get_client_ip(request)
    ua = request.headers.get("user-agent", "")[:500]

    await db.execute(
        text(
            "INSERT INTO tool_downloads (id, tool_id, downloaded_at, ip_address, user_agent) "
            "VALUES (:id, :tool_id, :ts, :ip, :ua)"
        ),
        {
            "id": str(uuid.uuid4()),
            "tool_id": tool_id,
            "ts": datetime.now(timezone.utc),
            "ip": ip,
            "ua": ua,
        },
    )
    await db.commit()

    result = await db.execute(
        text("SELECT COUNT(*) FROM tool_downloads WHERE tool_id = :tool_id"),
        {"tool_id": tool_id},
    )
    count = result.scalar_one()
    return DownloadRecordResponse(tool_id=tool_id, count=int(count), recorded=True)


@router.get("/{tool_id}", response_model=DownloadCountResponse)
async def get_download_count(
    tool_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        text("SELECT COUNT(*) FROM tool_downloads WHERE tool_id = :tool_id"),
        {"tool_id": tool_id},
    )
    count = result.scalar_one()
    return DownloadCountResponse(tool_id=tool_id, count=int(count))
