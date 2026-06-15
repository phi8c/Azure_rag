from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity_relationship import (
    EntityRelationship
)


class EntityRelationshipRepository:

    @staticmethod
    async def exists(

        db: AsyncSession,

        source_entity_id: int,

        target_entity_id: int

    ):

        result = await db.execute(

            select(EntityRelationship)

            .where(
                EntityRelationship
                .source_entity_id
                == source_entity_id
            )

            .where(
                EntityRelationship
                .target_entity_id
                == target_entity_id
            )
        )

        return (
            result
            .scalar_one_or_none()
        )

    @staticmethod
    async def create(

        db: AsyncSession,

        source_entity_id: int,

        target_entity_id: int,

        weight: float = 1.0

    ):

        relation = EntityRelationship(

            source_entity_id=
            source_entity_id,

            target_entity_id=
            target_entity_id,

            weight=weight
        )

        db.add(relation)

        await db.flush()

        return relation

    @staticmethod
    async def create_if_not_exists(

        db: AsyncSession,

        source_entity_id: int,

        target_entity_id: int

    ):

        relation = await (
            EntityRelationshipRepository
            .exists(
                db,
                source_entity_id,
                target_entity_id
            )
        )

        if relation:
            return relation

        return await (
            EntityRelationshipRepository
            .create(
                db,
                source_entity_id,
                target_entity_id
            )
        )