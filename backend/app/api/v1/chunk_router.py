"""Read-only access to chunks stored in Azure Search."""

from fastapi import APIRouter

from app.repositories.azure_chunk_repository import AzureChunkRepository


router = APIRouter(prefix="/chunks", tags=["Chunks"])


@router.get("/")
async def get_all_chunks(parent_id: str):
    chunks = AzureChunkRepository.load_chunks(parent_id)
    return {"total": len(chunks), "chunks": chunks}
