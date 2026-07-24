from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.ai_model_repository import (
    AIModelRepository,
)


class GetModelsService:

    @staticmethod
    async def execute(
        db: AsyncSession,
    ):
        return await AIModelRepository.get_all(
            db=db,
        )