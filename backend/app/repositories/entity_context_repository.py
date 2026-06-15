from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity_context import (
    EntityContext
)


class EntityContextRepository:

    @staticmethod
    async def create(
        db: AsyncSession,

        entity_id: int,

        chunk_id: str,

        summary: str,

        embedding: list[float]
    ):

        context = EntityContext(

            entity_id=entity_id,

            chunk_id=chunk_id,

            summary=summary,

            embedding=embedding
        )

        db.add(context)

        await db.flush()

        return context