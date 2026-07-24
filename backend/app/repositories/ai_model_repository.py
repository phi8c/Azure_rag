from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.ai_model import (
    AIModel
)
from uuid import UUID


class AIModelRepository:

    @staticmethod
    async def get_all(
        db: AsyncSession
    ):
        query = await db.execute(
            select(
                AIModel
            )
            .where(
                AIModel.is_active == True
            )
            .order_by(
                AIModel.display_name.asc()
            )
        )

        return (
            query
            .scalars()
            .all()
        )

    @staticmethod
    async def get_default(
        db: AsyncSession
    ):
        query = await db.execute(
            select(
                AIModel
            )
            .where(
                AIModel.is_default == True
            )
        )

        return (
            query
            .scalar_one_or_none()
        )

    @staticmethod
    async def get_by_code(
        db: AsyncSession,
        code: str
    ):
        query = await db.execute(
            select(
                AIModel
            )
            .where(
                AIModel.code == code
            )
        )

        return (
            query
            .scalar_one_or_none()
        )
        
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        id: UUID,
    ):
        query = await db.execute(
            select(
                AIModel
            )
            .where(
                AIModel.id == id,
                AIModel.is_active == True,
            )
        )

        return (
            query
            .scalar_one_or_none()
        )
        
    