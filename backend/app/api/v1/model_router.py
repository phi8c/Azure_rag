from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import Depends

from app.core.database import (
    get_db
)
from app.services.llm.get_model_service import (
    GetModelsService,
)

router = APIRouter(
    prefix="/models",
    tags=["Models"],
)


@router.get("")
async def get_models(
    db: AsyncSession = Depends(get_db),
):
    return await GetModelsService.execute(db)