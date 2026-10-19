import asyncio

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.services.knic_crawler import crawl_knic


router = APIRouter(prefix="/documents", tags=["Documents"])


class KnicCrawlRequest(BaseModel):
    max_pages: int = Field(default=30, ge=1, le=60)
    max_depth: int = Field(default=2, ge=0, le=4)


@router.post("/crawl/knic", response_class=Response)
async def crawl_knic_document(payload: KnicCrawlRequest = KnicCrawlRequest()):
    """Download KNIC text for manual SharePoint upload, then POST /documents/sync."""
    try:
        filename, content = await crawl_knic(payload.max_pages, payload.max_depth)
    except asyncio.TimeoutError as exc:
        raise HTTPException(504, "KNIC crawl exceeded 180 seconds; reduce max_pages") from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(502, "Unable to collect readable KNIC website content") from exc
    return Response(
        content=content, media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
