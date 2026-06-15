from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity import Entity


class EntityRepository:

    @staticmethod
    async def get_by_name(
        db: AsyncSession,
        name: str
    ):

        result = await db.execute(
            select(Entity)
            .where(Entity.name == name)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        db: AsyncSession,
        name: str
    ):

        entity = Entity(
            name=name
        )

        db.add(entity)

        await db.flush()

        return entity

    @staticmethod
    async def get_or_create(
        db: AsyncSession,
        name: str
    ):

        entity = await (
            EntityRepository
            .get_by_name(
                db,
                name
            )
        )

        if entity:
            return entity

        return await (
            EntityRepository
            .create(
                db,
                name
            )
        )